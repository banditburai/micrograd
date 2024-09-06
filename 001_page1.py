from fasthtml.common import *
from page_utils import TutorialPage, create_form, create_next_button
from starlette.requests import Request

page = TutorialPage("Page 1")

@page.step(1)
def step1(request: Request, form_data=None):
    return Div(
        P("Welcome to the first step of Page 1."),
        create_form(action="?step=2", name=("text", "Enter your name:", True))
    )

@page.step(2)
def step2(request: Request, form_data=None):
    name = form_data.get('name', 'Unknown') if form_data else request.query_params.get('name', 'Unknown')
    return Div(
        H2("Welcome!"),
        P(f"Hello, {name}! You've completed the first step of Page 1."),
        create_next_button(3, name=name)  # Pass the name as a hidden field
    )

@page.step(3)
def step3(request: Request, form_data=None):
    name = form_data.get('name', 'Unknown') if form_data else request.query_params.get('name', 'Unknown')
    return Div(
        H2("Final Step"),
        P(f"This is the final step of Page 1, {name}."),
        A("Next Page", href="/002_page2", hx_get="/002_page2", hx_target="#content", hx_push_url="/002_page2", cls="button")
    )

async def get(request: Request):
    return await page.handle_request(request)

async def post(request: Request, form_data):
    return await page.handle_request(request, form_data)