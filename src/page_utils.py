from fasthtml.common import *
from functools import wraps
from dataclasses import dataclass
import os
import importlib.util
import sys

@dataclass
class TutorialPage:
    file_name: str
    display_name: str
    steps: dict = None

    def __init__(self, file_name, display_name):
        self.file_name = file_name
        self.display_name = display_name
        self.steps = {}

    def step(self, step_number):
        def decorator(func):
            self.steps[step_number] = func
            return func
        return decorator

    async def handle_request(self, request=None, session=None, form_data=None):
        step = int(request.query_params.get('step', 1))
        if step in self.steps:
            return await self.steps[step](request=request, session=session, form_data=form_data)
        else:
            return P(f"Error: Step {step} not found")

def create_form(action, **fields):
    return Form(
        *[Label(f"{label}: ", Input(type=type, name=name, required=required, cls="input w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:border-gray-600 dark:text-white"))
          for name, (type, label, required) in fields.items()],
        Input(type="submit", value="Submit", cls="button w-full bg-blue-500 hover:bg-blue-600 text-white font-bold py-2 px-4 rounded mt-4"),
        action=action,
        method="post",
        cls="space-y-4"
    )

def create_next_button(next_step):
    return A("Next", href=f"?step={next_step}", hx_get=f"?step={next_step}", hx_target="#content", hx_push_url="true", cls="button bg-blue-500 hover:bg-blue-600 text-white font-bold py-2 px-4 rounded inline-block")

def get_tutorial_pages(directory='src'):
    page_modules = {}
    base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sys.path.insert(0, base_path)
    
    for filename in sorted(os.listdir(directory)):
        if filename.endswith('.py') and filename[0].isdigit():
            module_name = f"src.{filename[:-3]}"
            file_path = os.path.join(base_path, directory, filename)
            try:
                spec = importlib.util.spec_from_file_location(module_name, file_path)
                module = importlib.util.module_from_spec(spec)
                sys.modules[module_name] = module
                spec.loader.exec_module(module)
                
                page = getattr(module, 'page', None)
                if page and isinstance(page, TutorialPage):
                    page_modules[page.file_name] = page
                    print(f"Successfully imported {module_name}")
                else:
                    print(f"Warning: {module_name} does not contain a valid TutorialPage object")
            except Exception as e:
                print(f"Error importing {module_name}: {str(e)}")
    
    return page_modules