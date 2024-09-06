from fasthtml.common import *
from functools import wraps

class TutorialPage:
    def __init__(self, page_name):
        self.page_name = page_name
        self.steps = {}

    def step(self, step_number):
        def decorator(func):
            @wraps(func)
            def wrapper(request, form_data=None):
                content = func(request, form_data)
                return self.render_step(step_number, content)
            self.steps[step_number] = wrapper
            return wrapper
        return decorator

    def render_step(self, step_number, content):
        return Article(
            H1(f"{self.page_name} - Step {step_number}"),
            content,
            Div(id=f"step-{step_number}-content")
        )

    async def handle_request(self, request, form_data=None):
        step = int(request.query_params.get('step', '1'))
        if step in self.steps:
            return self.steps[step](request, form_data)
        return P(f"Error: Invalid step {step}")

def create_form(action, target="#content", swap="innerHTML", hidden_fields=None, **fields):
    form_content = []
    if hidden_fields:
        for name, value in hidden_fields.items():
            form_content.append(Input(type="hidden", name=name, value=value))
    for field_id, (field_type, label, required) in fields.items():
        if label:
            form_content.append(Label(label, For=field_id))
        form_content.append(Input(type=field_type, name=field_id, id=field_id, required=required))
    form_content.append(Button("Submit", type="submit"))
    return Form(
        *[item for item in form_content if item is not None],
        hx_post=action,
        hx_target=target,
        hx_swap=swap,
        hx_push_url=action
    )

def create_next_button(next_step, text="Next Step", **hidden_fields):
    form_fields = [Input(type="hidden", name=key, value=value) for key, value in hidden_fields.items()]
    return Form(
        *form_fields,
        Input(type="submit", value=text),
        action=f"?step={next_step}",
        method="POST",
        hx_post=f"?step={next_step}",
        hx_target="#content"
    )