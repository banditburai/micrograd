from fasthtml.common import *
from src.page_utils import TutorialPage, create_next_button, create_form, create_page_navigation

page = TutorialPage(
    page_number=3,
    display_name="Neural Networks Basics",
    slug="neural-networks-basics",
    markdown_file="src/markdown/003_neural_networks_basics.md"
)

@page.step(1)
async def step_1(request, form_data=None):
    return Div(
        *page.get_chunk_content(1, cls="text-2xl font-bold"),
        *page.get_chunk_content(2, cls="text-gray-600 dark:text-gray-400"),
        create_next_button(2),
        cls="bg-white dark:bg-gray-800 shadow-md rounded-lg p-6 max-w-md mx-auto"
    )

@page.step(2)
async def step_2(request, form_data=None):
    return Div(
        *page.get_chunk_content(3),
        create_form("?step=3", neural_network_components=("text", "List the main components of a neural network:", True)),
        cls="bg-white dark:bg-gray-800 shadow-md rounded-lg p-6 max-w-md mx-auto"
    )

@page.step(3)
async def step_3(request, form_data=None):
    if form_data and 'neural_network_components' in form_data:
        user_answer = form_data['neural_network_components'].lower()
        required_components = ['input', 'hidden', 'output']
        if all(component in user_answer for component in required_components):
            return Div(
                *page.get_chunk_content(4),
                P("Great job! You correctly identified the main components of a neural network.", 
                  cls="text-green-600 dark:text-green-400"),
                create_next_button(4),
                cls="bg-white dark:bg-gray-800 shadow-md rounded-lg p-6 max-w-md mx-auto"
            )
        else:
            return Div(
                P("Not quite. Please try again and make sure to include input, hidden, and output layers.", 
                  cls="text-red-600 dark:text-red-400"),
                create_form("?step=3", neural_network_components=("text", "List the main components of a neural network:", True)),
                cls="bg-white dark:bg-gray-800 shadow-md rounded-lg p-6 max-w-md mx-auto"
            )
    else:
        return Div(
            *page.get_chunk_content(3),
            create_form("?step=3", neural_network_components=("text", "List the main components of a neural network:", True)),
            cls="bg-white dark:bg-gray-800 shadow-md rounded-lg p-6 max-w-md mx-auto"
        )

@page.step(4)
async def step_4(request, form_data=None):
    return Div(
        *page.get_chunk_content(5, cls="text-blue-600 dark:text-blue-400"),
        create_form("?step=5", backpropagation_explanation=("textarea", "Explain backpropagation in your own words:", True)),
        cls="bg-white dark:bg-gray-800 shadow-md rounded-lg p-6 max-w-md mx-auto"
    )

@page.step(5)
async def step_5(request, form_data=None):
    if form_data and 'backpropagation_explanation' in form_data:
        explanation = form_data['backpropagation_explanation']
        if len(explanation.split()) < 2:
            return Div(
                P("Your explanation is too short. Please provide a more detailed explanation.", 
                  cls="text-red-600 dark:text-red-400"),
                create_form("?step=5", backpropagation_explanation=("textarea", "Explain backpropagation in your own words:", True)),
                cls="bg-white dark:bg-gray-800 shadow-md rounded-lg p-6 max-w-md mx-auto"
            )
        else:
            return Div(
                *page.get_chunk_content(6),
                P(f"Your explanation: {explanation}", 
                  cls="mt-4 p-2 bg-gray-100 dark:bg-gray-700 rounded"),
                create_next_button(6),
                cls="bg-white dark:bg-gray-800 shadow-md rounded-lg p-6 max-w-md mx-auto"
            )
    else:
        return Div(
            *page.get_chunk_content(5),
            create_form("?step=5", backpropagation_explanation=("textarea", "Explain backpropagation in your own words:", True)),
            cls="bg-white dark:bg-gray-800 shadow-md rounded-lg p-6 max-w-md mx-auto"
        )

@page.step(6)
async def step_6(request, form_data=None):
    return Div(
        *page.get_chunk_content(7),
        create_page_navigation(request, page),
        cls="bg-white dark:bg-gray-800 shadow-md rounded-lg p-6 max-w-md mx-auto"
    )

