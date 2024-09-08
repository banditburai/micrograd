import importlib
import pkgutil
from fasthtml.common import *
from dataclasses import dataclass

@dataclass
class TutorialPage:
    page_number: int
    display_name: str
    slug: str
    published: bool = True
    steps: dict = None

    def __init__(self, page_number, display_name, slug, published=True):
        self.page_number = page_number
        self.display_name = display_name
        self.slug = slug
        self.published = published
        self.steps = {}

    def step(self, step_number):
        def decorator(func):
            self.steps[step_number] = func
            return func
        return decorator

    async def handle_request(self, request, form_data=None):
        step = int(request.query_params.get('step', 1))
        if step in self.steps:
            if form_data is not None:
                return await self.steps[step](request, form_data)
            else:
                return await self.steps[step](request)
        else:
            return P(f"Error: Step {step} not found")

def create_form(action, **fields):
    return Form(
        *[Label(f"{label}: ", Input(type=type, name=name, required=required, cls="input w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:border-gray-600 dark:text-white"))
          for name, (type, label, required) in fields.items()],
        Input(type="submit", value="Submit", cls="button w-full bg-blue-500 hover:bg-blue-600 text-white font-bold py-2 px-4 rounded mt-4"),
        hx_post=action,
        method="post",
        hx_target="#content",
        hx_push_url="true",
        cls="space-y-4"
    )

def create_next_button(next_step):
    return A("Next", 
             href=f"?step={next_step}", 
             hx_get=f"?step={next_step}", 
             hx_target="#content", 
             hx_push_url="true", 
             cls="button bg-blue-500 hover:bg-blue-600 text-white font-bold py-2 px-4 rounded inline-block")

def create_page_navigation(request, current_page):
    pages = list(request.app.state.page_modules.values())
    current_index = next(i for i, p in enumerate(pages) if p.slug == current_page.slug)
    next_page = pages[current_index + 1] if current_index + 1 < len(pages) else None
    
    if next_page:
        return A("Next Page", href=f"/{next_page.slug}", hx_get=f"/{next_page.slug}", hx_target="#content", hx_push_url=f"/{next_page.slug}", 
                 cls="bg-blue-500 hover:bg-blue-600 text-white font-bold py-2 px-4 rounded inline-block")
    else:
        return P(f"Congratulations! You've completed the {current_page.display_name} section.", 
                 cls="text-lg font-semibold text-green-600 dark:text-green-400")

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