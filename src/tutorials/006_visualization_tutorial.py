from fasthtml.common import *
from src.page_utils import TutorialPage, create_next_button, create_page_navigation

page = TutorialPage(
    page_number=6,
    display_name="Visualization Tutorial",
    slug="visualization-tutorial",
)

# Common classes for page content
page_classes = "bg-white dark:bg-gray-800 shadow-md rounded-lg p-6 max-w-md mx-auto"

@page.step(1)
async def step_1(request, form_data=None):
    return Div(
        H1("Welcome to the Visualization Tutorial", cls="text-3xl font-bold mb-4 text-gray-900 dark:text-white"),
        P("In this tutorial, we will explore different types of visualizations.", cls="mb-4 text-gray-700 dark:text-gray-300"),
        create_next_button(2),
        cls=page_classes
    )

@page.step(2)
async def step_2(request, form_data=None):
    return Div(
        H2("Why Visualizations?", cls="text-2xl font-semibold mb-3 text-gray-900 dark:text-white"),
        P("Visualizations help us understand data better by providing a visual context.", cls="mb-4 text-gray-700 dark:text-gray-300"),
        create_next_button(3),
        cls=page_classes
    )

@page.step(3)
async def step_3(request, form_data=None):
    return Div(
        H2("Types of Visualizations", cls="text-2xl font-semibold mb-3 text-gray-900 dark:text-white"),
        P("Common types of visualizations include:", cls="mb-4 text-gray-700 dark:text-gray-300"),
        Ul(
            Li("Bar Charts", cls="mb-2"),
            Li("Line Graphs", cls="mb-2"),
            Li("Pie Charts", cls="mb-2"),
            Li("Scatter Plots", cls="mb-2"),
            cls="list-disc list-inside mb-4 text-gray-700 dark:text-gray-300"
        ),
        create_next_button(4),
        cls=page_classes
    )

@page.step(4)
async def step_4(request, form_data=None):
    return Div(
        H2("Creating a Simple Visualization", cls="text-2xl font-semibold mb-3 text-gray-900 dark:text-white"),
        P("In the next step, we will create a simple D3 visualization.", cls="mb-4 text-gray-700 dark:text-gray-300"),
        create_next_button(5),
        cls=page_classes
    )

@page.step(5)
async def step_5(request, form_data=None):
    return Div(
        H2("D3 Visualization Example", cls="text-2xl font-semibold mb-3 text-gray-900 dark:text-white"),
        P("Click the button below to load the D3 visualization:", cls="mb-4 text-gray-700 dark:text-gray-300"),
        Button("Load Visualization", 
               hx_get="/example", 
               hx_target="#visualization-container", 
               hx_swap="innerHTML", 
               cls="bg-blue-500 hover:bg-blue-600 text-white font-bold py-2 px-4 rounded"),
        Div(id="visualization-container", cls="w-full h-[400px] border border-gray-300"),  # Container for the visualization
        Button("Show Additional Information", 
               hx_get="?step=6",  # Link to Step 6
               hx_target="#content", 
               hx_swap="innerHTML", 
               cls="bg-green-500 hover:bg-green-600 text-white font-bold py-2 px-4 rounded"),
        create_page_navigation(request, page),
        cls=page_classes
    )

@page.step(6)
async def step_6(request, form_data=None):
    return Div(
        H2("Additional Information", cls="text-2xl font-semibold mb-3 text-gray-900 dark:text-white"),
        P("Here is some additional information related to the visualization.", cls="mb-4 text-gray-700 dark:text-gray-300"),
        P("You can explore more about D3 visualizations and their applications.", cls="mb-4 text-gray-700 dark:text-gray-300"),
        Button("Back to Visualization", 
               hx_get="?step=5",  # Assuming step 5 is the visualization step
               hx_target="#content", 
               hx_swap="innerHTML", 
               cls="bg-blue-500 hover:bg-blue-600 text-white font-bold py-2 px-4 rounded"),
        cls=page_classes
    )
