from fasthtml.common import *
from src.page_utils import TutorialPage, create_form, create_next_button, create_page_navigation
from starlette.requests import Request

page = TutorialPage(2, "Basic Concepts", "basic-concepts")

@page.step(1)
async def step1(request: Request, form_data=None):
    return Div(
        H1("Basic Concepts in Machine Learning", cls="text-3xl font-bold mb-4 text-gray-900 dark:text-white"),
        P("In this section, we'll cover some fundamental concepts in machine learning.", cls="mb-4 text-gray-700 dark:text-gray-300"),
        H2("What is Machine Learning?", cls="text-2xl font-semibold mb-3 text-gray-900 dark:text-white"),
        P("Machine Learning is a subset of artificial intelligence that focuses on the development of algorithms and statistical models that enable computer systems to improve their performance on a specific task through experience.", 
          cls="mb-4 text-gray-700 dark:text-gray-300"),
        create_next_button(2),
        cls="bg-white dark:bg-gray-800 shadow-md rounded-lg p-6 max-w-md mx-auto"
    )

@page.step(2)
async def step2(request: Request, form_data=None):
    return Div(
        H2("Types of Machine Learning", cls="text-2xl font-semibold mb-3 text-gray-900 dark:text-white"),
        Ul(
            Li("Supervised Learning", cls="mb-2"),
            Li("Unsupervised Learning", cls="mb-2"),
            Li("Reinforcement Learning", cls="mb-2"),
            cls="list-disc list-inside mb-4 text-gray-700 dark:text-gray-300"
        ),
        P("In this tutorial, we'll focus primarily on supervised learning.", cls="mb-4 text-gray-700 dark:text-gray-300"),
        create_form(action="?step=3", 
                    answer=("text", "What type of learning involves labeled data?", True), 
                    ),
        cls="bg-white dark:bg-gray-800 shadow-md rounded-lg p-6 max-w-md mx-auto"
    )

@page.step(3)
async def step3(request: Request, form_data=None):
    answer = form_data.get('answer', '').lower() if form_data else ''
    is_correct = 'supervised' in answer
    
    content = [
        H2("Supervised Learning", cls="text-2xl font-semibold mb-3 text-gray-900 dark:text-white"),
        P("Supervised learning is a type of machine learning where the algorithm learns from labeled training data.", 
          cls="mb-4 text-gray-700 dark:text-gray-300"),
    ]
    
    if is_correct:
        content.append(P("Great job! You correctly identified supervised learning.", 
                         cls="mb-4 text-green-600 dark:text-green-400"))
    else:
        content.append(P("The correct answer is supervised learning. Let's learn more about it.", 
                         cls="mb-4 text-red-600 dark:text-red-400"))
    
    content.append(create_next_button(4))
    
    return Div(*content, cls="bg-white dark:bg-gray-800 shadow-md rounded-lg p-6 max-w-md mx-auto")

@page.step(4)
async def step4(request: Request, form_data=None):
    content = [
        H2("Recap", cls="text-2xl font-semibold mb-3 text-gray-900 dark:text-white"),
        P("In this section, we covered:", cls="mb-4 text-gray-700 dark:text-gray-300"),
        Ul(
            Li("The definition of Machine Learning", cls="mb-2"),
            Li("Types of Machine Learning", cls="mb-2"),
            Li("Introduction to Supervised Learning", cls="mb-2"),
            cls="list-disc list-inside mb-4 text-gray-700 dark:text-gray-300"
        ),
        P("In the next section, we'll dive deeper into the components of a neural network.", 
          cls="mb-4 text-gray-700 dark:text-gray-300"),
        create_page_navigation(request, page)
    ]
    
    return Div(*content, cls="bg-white dark:bg-gray-800 shadow-md rounded-lg p-6 max-w-md mx-auto")
