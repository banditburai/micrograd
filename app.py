from fasthtml.common import *
import importlib
import os
import sys
import traceback
from starlette.responses import PlainTextResponse

app, rt = fast_app(    
    hdrs=(
        Script(src="https://cdn.jsdelivr.net/npm/d3@7")                
    )
)

# Dynamically import all page modules
page_modules = {}
for filename in sorted(os.listdir('.')):
    if filename.endswith('.py') and filename[0].isdigit():
        module_name = filename[:-3]  # Remove .py extension
        try:
            page_modules[module_name] = importlib.import_module(module_name)
            print(f"Successfully imported {module_name}")
        except Exception as e:
            print(f"Error importing {module_name}: {str(e)}", file=sys.stderr)

def create_nav():
    nav_items = [Li(A("Home", href="/", hx_get="/", hx_target="#content", hx_push_url="/"))]
    for filename in sorted(os.listdir('.')):
        if filename.endswith('.py') and filename[0].isdigit():
            page_name = filename[:-3]  # Remove .py extension
            nav_items.append(Li(A(page_name, href=f"/{page_name}", hx_get=f"/{page_name}", hx_target="#content", hx_push_url=f"/{page_name}")))
    return Nav(Ul(*nav_items))

def create_layout(content):
    return Div(
        Header(
            create_nav(),
            Button("Toggle Theme", 
                   onclick="document.documentElement.setAttribute('data-theme', document.documentElement.getAttribute('data-theme') === 'light' ? 'dark' : 'light');", 
                   cls="contrast outline")
        ),
        Main(Div(content, id="content")),
        Footer(P("© 2024 Tutorial"))
    )

@app.exception_handler(Exception)
async def exception_handler(request, exc):
    print(f"An error occurred: {str(exc)}")
    print("Traceback:")
    traceback.print_exc()
    return PlainTextResponse(f"An error occurred: {str(exc)}", status_code=500)

@rt('/')
def get(request):
    home_content = Article(
        H1("Tutorial Home"),
        P("Welcome to the tutorial. Click 'Start' to begin."),
        A("Start", href="/001_page1", hx_get="/001_page1", hx_target="#content", hx_push_url="/001_page1", cls="button")
    )
    if request.headers.get('HX-Request') == 'true':
        return home_content
    return Titled("Tutorial", create_layout(home_content))

@rt('/{module_name}')
async def page_handler(module_name: str, request: Request):
    module = page_modules.get(module_name)
    if module is None:
        return P(f"Error: Module {module_name} not found")
    
    if request.method == 'GET':
        content = await module.get(request)
    elif request.method == 'POST':
        form_data = await request.form()
        content = await module.post(request, form_data)
    else:
        return P(f"Error: Unsupported method {request.method}")

    if request.headers.get('HX-Request') == 'true':
        return content
    return Titled(f"Tutorial - {module_name}", create_layout(content))

serve()
