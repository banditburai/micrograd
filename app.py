from fasthtml.common import *
import traceback
from starlette.responses import PlainTextResponse
from fasthtml.svg import *
from components.theme_toggle import ThemeToggle, HamburgerMenu, fouc_script, dark_mode_toggle_script
from src.page_utils import get_tutorial_pages, get_last_page


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
                min-width: 320px;  /* Set a minimum width for the app */
            }
        """)
    )
)

# Dynamically import all page modules
page_modules = get_tutorial_pages()
last_page = get_last_page(page_modules)

app.state.page_modules = page_modules

def CommonHeader():
    return Header(
        Div(
            Div(                
                A("Micrograd", href="/", hx_get="/", hx_target="#content", hx_push_url="/", 
                  cls="text-2xl font-bold text-gray-900 dark:text-white"),
                cls="flex-grow"
            ),
            Div(
                ThemeToggle(),
                cls="hidden md:block"  # Hide on mobile, show on larger screens
            ),
            cls="flex justify-between items-center h-16 px-4 bg-gradient-to-b from-slate-300 via-slate-200 to-transparent dark:from-gray-700 dark:via-gray-800 dark:to-transparent shadow-md"
        ),
        cls="h-16"  # Fixed height for the header
    )

def create_nav(current_slug=None):
    nav_items = [
        Li(A(page.display_name, 
            href=f"/{page.slug}", 
            hx_get=f"/{page.slug}", 
            hx_target="#content", 
            hx_push_url="true", 
            cls=f"nav-link {'selected' if page.slug == current_slug else ''}"))
        for page in sorted(page_modules.values(), key=lambda p: p.page_number)
    ]

    return Div(
        # Desktop navigation
        Nav(
            Ul(*nav_items, cls="hidden md:flex md:space-x-2"),
            cls="nav-container md:block px-4 hover:bg-gray-100 dark:hover:bg-gray-800 md:hover:bg-gray-100 md:dark:hover:bg-gray-800"
        ),
        # Mobile navigation (sidebar)
        Div(
            HamburgerMenu(),
            Aside(
                Nav(
                    *[Div(A(page.display_name, 
                        href=f"/{page.slug}", 
                        hx_get=f"/{page.slug}", 
                        hx_target="#content", 
                        hx_push_url="true", 
                        cls=f"text-gray-300 hover:text-white block py-2 {'selected' if page.slug == current_slug else ''}"))
                    for page in sorted(page_modules.values(), key=lambda p: p.page_number)],
                    Div(ThemeToggle(), cls="mt-4"),
                ),
                cls="sidebar md:hidden"
            ),
            cls="md:hidden absolute top-0 right-0 m-4"  # Position hamburger menu
        ),
        id="navigation",
        cls="h-12 md:h-12"  # Fixed height on both mobile and desktop
    )

def create_layout(content=None, current_slug=None):
    return Div(
        CommonHeader(),
        create_nav(current_slug),
        Main(Div(content or "", id="content", cls="p-4 max-w-4xl mx-auto flex-grow")),
        Footer(
            P("© 2024 Tutorial", cls="text-center p-4 text-gray-600 dark:text-gray-300"),
            cls="mt-auto bg-gradient-to-t from-slate-300 via-slate-200 to-transparent dark:from-gray-700 dark:via-gray-800 dark:to-transparent h-16"
        ),
        cls="min-h-screen flex flex-col"
    )

@rt('/')
def get(request):
    if not page_modules:
        content = Div(
            H1("No Tutorial Pages Available", cls="text-3xl font-bold mb-4 text-gray-900 dark:text-white"),
            P("There are currently no published tutorial pages.", cls="mb-4 text-gray-700 dark:text-gray-300"),
            cls="bg-white dark:bg-gray-800 shadow-md rounded-lg p-6 max-w-md mx-auto"
        )
    else:
        first_page = sorted(page_modules.values(), key=lambda p: p.page_number)[0]
        content = Article(
            H1("Micrograd Tutorial", cls="text-3xl font-bold mb-4 text-gray-900 dark:text-white"),
            P("Let's get started.", cls="mb-4 text-gray-300 dark:text-gray-300"),
            A("Start", 
              href=f"/{first_page.slug}", 
              cls="bg-blue-500 hover:bg-blue-600 text-white font-bold py-2 px-4 rounded inline-block"),
            hx_get=f"/{first_page.slug}",
            hx_target="#content",
            hx_push_url=f"/{first_page.slug}",
            hx_trigger="click",
            cls="bg-blue-500 hover:bg-blue-600 text-white font-bold py-6 px-8 rounded cursor-pointer transition duration-300 flex flex-col items-center justify-center max-w-md mx-auto",
        )
    
    if request.headers.get('HX-Request') == 'true':
        updated_nav = create_nav(current_slug=None)  # No slug is selected on the home page
        return (
            content,
            Div(updated_nav, id="navigation", hx_swap_oob="true")
        )
    
    return Title("Micrograd Tutorial"), create_layout(content)

@rt('/{slug}')
async def page_handler(slug: str, request: Request):
    page = page_modules.get(slug)
    if page is None:
        return create_404_page()
    
    if request.method == 'GET':
        content = await page.handle_request(request)
    elif request.method == 'POST':
        form_data = await request.form()
        content = await page.handle_request(request, form_data)
    else:
        return P(f"Error: Unsupported method {request.method}")

    if request.headers.get('HX-Request') == 'true':
        updated_nav = create_nav(current_slug=slug)
        return (
            content,
            Div(updated_nav, id="navigation", hx_swap_oob="true")
        )
    
    return Title(f"{page.display_name}"), create_layout(content, slug)

def create_404_page():
    return Div(
        H1("404 - Page Not Found", cls="text-3xl font-bold mb-4 text-gray-900 dark:text-white"),
        P("The page you're looking for doesn't exist.", cls="mb-4 text-gray-700 dark:text-gray-300"),
        A("Go Home", href="/", hx_get="/", hx_target="#content", hx_push_url="/", 
          cls="bg-blue-500 hover:bg-blue-600 text-white font-bold py-2 px-4 rounded inline-block"),
        cls="bg-white dark:bg-gray-800 shadow-md rounded-lg p-6 max-w-md mx-auto"
    )

@app.exception_handler(Exception)
async def exception_handler(request, exc):
    print(f"An error occurred: {str(exc)}")
    print("Traceback:")
    traceback.print_exc()
    return PlainTextResponse(f"An error occurred: {str(exc)}", status_code=500)


serve()

