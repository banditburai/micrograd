from fasthtml.common import *
import traceback
from starlette.responses import PlainTextResponse
from fasthtml.svg import *
from components.theme_toggle import ThemeToggle, fouc_script, dark_mode_toggle_script
from src.page_utils import get_tutorial_pages

tailwindLink = Link(rel="stylesheet", href="assets/output.css", type="text/css")
app, rt = fast_app(
    pico=False,
    hdrs=(
        fouc_script,
        tailwindLink,
        Script(src="https://cdn.jsdelivr.net/npm/d3@7"),
        Script(dark_mode_toggle_script),
        Style("""
            body {
                overscroll-behavior: none;
                overflow-x: hidden;
                touch-action: pan-y;
            }
        """)
    )
)

# Dynamically import all page modules
page_modules = get_tutorial_pages('src')

def CommonHeader():
    return Header(
        Div(
            Div(
                A("Tutorial", href="/", hx_get="/", hx_target="#content", hx_push_url="/", 
                  cls="text-2xl font-bold text-gray-900 dark:text-white"),
                cls="flex-grow"
            ),
            ThemeToggle(),
            cls="flex justify-between items-center mb-4 p-4 bg-white dark:bg-gray-800 shadow"
        )
    )

def create_nav():
    return Nav(
        Ul(
            *[Li(A(page.display_name, 
                   href=f"/{page.file_name}", 
                   hx_get=f"/{page.file_name}", 
                   hx_target="#content", 
                   hx_push_url=f"/{page.file_name}", 
                   cls="text-gray-600 hover:text-gray-900 dark:text-gray-300 dark:hover:text-white px-3 py-2 rounded-md text-sm font-medium"))
              for page in sorted(page_modules.values(), key=lambda p: p.file_name)],
            cls="flex flex-wrap space-x-2 md:space-x-4"
        ),
        cls="p-4 bg-gray-100 dark:bg-gray-700 overflow-x-auto"
    )

def create_layout(content, title):
    return Div(
        CommonHeader(),
        create_nav(),
        Main(Div(content, id="content", cls="p-4 max-w-4xl mx-auto")),
        Footer(P("© 2024 Tutorial", cls="text-center p-4 bg-white dark:bg-gray-800 text-gray-600 dark:text-gray-300")),
        cls="min-h-screen flex flex-col"
    )

@rt('/')
def get(request):
    home_content = Article(
        H1("Tutorial Home", cls="text-3xl font-bold mb-4 text-gray-900 dark:text-white"),
        P("Welcome to the tutorial. Click 'Start' to begin.", cls="mb-4 text-gray-700 dark:text-gray-300"),
        A("Start", href="/001_getting_started", hx_get="/001_getting_started", hx_target="#content", hx_push_url="/001_getting_started", 
        cls="bg-blue-500 hover:bg-blue-600 text-white font-bold py-2 px-4 rounded inline-block"),        
    )
    if request.headers.get('HX-Request') == 'true':
        return home_content
    return Title("Tutorial Home"), create_layout(home_content, "Tutorial Home")

@rt('/{module_name}')
async def page_handler(module_name: str, request: Request):
    page = page_modules.get(module_name)
    if page is None:
        return P(f"Error: Module {module_name} not found")
    
    if request.method == 'GET':
        content = await page.handle_request(request)
    elif request.method == 'POST':
        form_data = await request.form()
        content = await page.handle_request(request, form_data)
    else:
        return P(f"Error: Unsupported method {request.method}")

    page_title = f"Tutorial - {page.display_name}"
    if request.headers.get('HX-Request') == 'true':
        return content
    return Title(page_title), create_layout(content, page_title)

@app.exception_handler(Exception)
async def exception_handler(request, exc):
    print(f"An error occurred: {str(exc)}")
    print("Traceback:")
    traceback.print_exc()
    return PlainTextResponse(f"An error occurred: {str(exc)}", status_code=500)

serve()
