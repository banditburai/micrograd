import importlib
import pkgutil
from fasthtml.common import *
from dataclasses import dataclass, field
from src.markdown_utils import parse_markdown_file, markdown_to_fasthtml

@dataclass
class TutorialPage:
    page_number: int
    display_name: str
    slug: str
    published: bool = True
    markdown_file: str = None
    chunks: dict = field(default_factory=dict)
    steps: dict = field(default_factory=dict)

    def __post_init__(self):
        if self.markdown_file:
            self._load_markdown()

    def _load_markdown(self):
        self.chunks = parse_markdown_file(self.markdown_file)

    def step(self, step_number):
        def decorator(func):
            self.steps[step_number] = func
            return func
        return decorator

    async def handle_request(self, request, form_data=None):
        step = int(request.query_params.get('step', 1))
        if step in self.steps:
            return await self.steps[step](request, form_data)
        else:
            return P(f"Error: Step {step} not found")

    def get_chunk_content(self, chunk_number: int, cls: str = "") -> List[FT]:
        if chunk_number in self.chunks:
            return markdown_to_fasthtml(self.chunks[chunk_number], cls)
        else:
            return [P(f"Error: Chunk {chunk_number} not found")]

def create_form_field(name, type, label, required):
    field_cls = "w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:border-gray-600 dark:text-white"
    
    if type == "textarea":
        return Label(f"{label}: ", Textarea(name=name, required=required, cls=field_cls))
    elif type == "hidden":
        return Input(type="hidden", name=name)
    else:
        return Label(f"{label}: ", Input(type=type, name=name, required=required, cls=field_cls))

def create_form(action, **fields):    
    form_fields = []
    
    for name, field_info in fields.items():
        if len(field_info) == 3:
            form_fields.append(create_form_field(name, field_info[0], field_info[1], field_info[2]))
        else:
            raise ValueError(f"Field '{name}' must have exactly 3 elements: (type, label, required)")

    return Form(
        *form_fields,
        Input(type="submit", value="Submit", cls="w-full bg-blue-500 hover:bg-blue-600 text-white font-bold py-2 px-4 rounded mt-4"),
        action=action,
        method="post", 
        cls="space-y-4",
        hx_post=action, 
        hx_target="#content", 
        hx_swap="innerHTML" 
    )

def create_navigation_link(text, href, hx_get, hx_target, hx_push_url):
    return A(text, 
             href=href, 
             hx_get=hx_get, 
             hx_target=hx_target, 
             hx_push_url=hx_push_url, 
             cls="bg-blue-500 hover:bg-blue-600 text-white font-bold py-2 px-4 rounded inline-block")

def create_next_button(next_step):
    return create_navigation_link("Next", f"?step={next_step}", f"?step={next_step}", "#content", "true")

def create_page_navigation(request, current_page):
    pages = list(request.app.state.page_modules.values())
    current_index = next(i for i, p in enumerate(pages) if p.slug == current_page.slug)
    next_page = pages[current_index + 1] if current_index + 1 < len(pages) else None
    
    if next_page:
        return create_navigation_link("Next Page", f"/{next_page.slug}", f"/{next_page.slug}", "#content", f"/{next_page.slug}")
    else:
        return Div(
            P(f"Congratulations! You've completed the {current_page.display_name} section.", 
              cls="text-lg font-semibold text-green-600 dark:text-green-400"),
            A("Back to Home", href="/", hx_get="/", hx_target="#content", hx_push_url="/",
              cls="mt-4 bg-blue-500 hover:bg-blue-600 text-white font-bold py-2 px-4 rounded inline-block"),
            cls="text-center"
        )

def get_tutorial_pages():
    from src import tutorials
    page_modules = {}
    
    for _, module_name, _ in pkgutil.iter_modules(tutorials.__path__):
        module = importlib.import_module(f'src.tutorials.{module_name}')
        if hasattr(module, 'page') and isinstance(module.page, TutorialPage):
            if module.page.published:
                page_modules[module.page.slug] = module.page
                print(f"Successfully imported {module_name}")
            else:
                print(f"Page {module_name} is not published")
        else:
            print(f"Warning: {module_name} does not contain a valid TutorialPage object")
    
    return dict(sorted(page_modules.items(), key=lambda item: item[1].page_number))

def get_last_page(page_modules):
    return list(page_modules.values())[-1] if page_modules else None