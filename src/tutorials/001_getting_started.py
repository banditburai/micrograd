from fasthtml.common import *
from src.page_utils import TutorialPage, create_form, create_next_button, create_page_navigation
from starlette.requests import Request

page = TutorialPage(1, "Getting Started", "getting-started")

# Common classes for page content
page_classes = "bg-white dark:bg-gray-800 shadow-md rounded-lg p-6 max-w-md mx-auto"

@page.step(1)
async def step1(request: Request, form_data=None):
    return Div(
        H1("Welcome to Getting Started", cls="text-3xl font-bold mb-4 text-gray-900 dark:text-white"),
        P("This is the first step of Getting Started.", cls="mb-4 text-gray-700 dark:text-gray-300"),
        create_form(action="?step=2", name=("text", "Enter your name", True)),
        cls=page_classes
    )

@page.step(2)
async def step2(request: Request, form_data=None):
    if form_data and 'name' in form_data:
        request.session['name'] = form_data['name']
    name = request.session.get('name', 'Unknown')
    return Div(
        H2("Welcome!", cls="text-2xl font-semibold mb-3 text-gray-900 dark:text-white"),
        P(f"Hello, {name}! You've completed the first step of Getting Started.", cls="mb-4 text-gray-700 dark:text-gray-300"),
        create_next_button(3),
        cls=page_classes
    )

@page.step(3)
async def step3(request: Request, form_data=None):
    name = request.session.get('name', 'Unknown')
    content = [
        H2("Final Step", cls="text-2xl font-semibold mb-3 text-gray-900 dark:text-white"),
        P(f"This is the final step of Getting Started, {name}.", cls="mb-4 text-gray-700 dark:text-gray-300"),
        P("In this section, we covered:", cls="mb-4 text-gray-700 dark:text-gray-300"),
        Ul(
            Li("Introduction to the tutorial", cls="mb-2"),
            Li("Personalizing the experience with your name", cls="mb-2"),
            Li("Navigating through multiple steps", cls="mb-2"),
            cls="list-disc list-inside mb-4 text-gray-700 dark:text-gray-300"
        ),
        P("In the next section, we'll dive into some basic concepts of machine learning.", 
          cls="mb-4 text-gray-700 dark:text-gray-300"),
        create_page_navigation(request, page)
    ]
    
    return Div(*content, cls=page_classes)