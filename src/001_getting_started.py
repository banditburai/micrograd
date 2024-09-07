from fasthtml.common import *
from src.page_utils import TutorialPage, create_form, create_next_button
from starlette.requests import Request

page = TutorialPage("001_getting_started", "Getting Started")

@page.step(1)
async def step1(request: Request, session, form_data=None):
    return Div(
        H1("Welcome to Getting Started", cls="text-3xl font-bold mb-4 text-gray-900 dark:text-white"),
        P("This is the first step of Getting Started.", cls="mb-4 text-gray-700 dark:text-gray-300"),
        create_form(action="?step=2", name=("text", "Enter your name", True)),
        cls="bg-white dark:bg-gray-800 shadow-md rounded-lg p-6 max-w-md mx-auto"
    )

@page.step(2)
async def step2(request: Request, session, form_data=None):
    if form_data and 'name' in form_data:
        if session is not None:
            session['name'] = form_data['name']
        else:
            print("Warning: Session is None, unable to store name")
    name = session.get('name', 'Unknown') if session else 'Unknown'
    return Div(
        H2("Welcome!", cls="text-2xl font-semibold mb-3 text-gray-900 dark:text-white"),
        P(f"Hello, {name}! You've completed the first step of Getting Started.", cls="mb-4 text-gray-700 dark:text-gray-300"),
        create_next_button(3),
        cls="bg-white dark:bg-gray-800 shadow-md rounded-lg p-6 max-w-md mx-auto"
    )

@page.step(3)
async def step3(request: Request, session, form_data=None):
    name = session.get('name', 'Unknown') if session else 'Unknown'
    return Div(
        H2("Final Step", cls="text-2xl font-semibold mb-3 text-gray-900 dark:text-white"),
        P(f"This is the final step of Getting Started, {name}.", cls="mb-4 text-gray-700 dark:text-gray-300"),
        A("Next Page", href="/002_page2", hx_get="/002_page2", hx_target="#content", hx_push_url="/002_page2", 
          cls="bg-blue-500 hover:bg-blue-600 text-white font-bold py-2 px-4 rounded inline-block"),
        cls="bg-white dark:bg-gray-800 shadow-md rounded-lg p-6 max-w-md mx-auto"
    )