from fasthtml.common import *
from fasthtml.svg import *
from src.page_utils import TutorialPage, create_next_button, create_form, create_page_navigation
from src.visualizations.yin_yang_viz import create_yin_yang_chart, generate_yin_yang_data

page = TutorialPage(
    page_number=4,
    display_name="Yin-Yang Visualization",
    slug="yin-yang-visualization",
    markdown_file="src/markdown/004_yin_yang_visualization.md"
)

# Common classes for page content
page_classes = "bg-white dark:bg-gray-800 shadow-md rounded-lg p-6 w-full max-w-4xl mx-auto"

def create_yin_yang_svg(fill_color='#FFFFFF'):
    return Svg(
        Circle(cx='42.264', cy='42.263', r='5.443', fill=fill_color),
        Path(d='M32 2C15.458 2 2 15.458 2 32s13.458 30 30 30 30-13.458 30-30S48.542 2 32 2m-6.416 23.584a5.444 5.444 0 1 1-7.699-7.7 5.444 5.444 0 0 1 7.699 7.7m20.501 30.675c-4.859 1.321-10.27.086-14.086-3.729-5.668-5.668-5.668-14.86 0-20.529s5.669-14.86 0-20.528c-3.815-3.816-9.225-5.052-14.084-3.73A27.9 27.9 0 0 1 32 3.936c15.476 0 28.064 12.589 28.064 28.064 0 10.344-5.628 19.391-13.979 24.259', fill=fill_color),
        width='50',
        height='50',
        viewbox='0 0 64 64',
        xmlns='http://www.w3.org/2000/svg',
        aria_hidden='true',
        cls='iconify iconify--emojione-monotone mb-4'
    )

@page.step(1)
async def step_1(request, form_data=None):
    request.session['visible_controls'] = []
    return Div(
        *page.get_chunk_content(1, cls="text-2xl font-bold"),
        *page.get_chunk_content(2, cls="text-gray-600 dark:text-gray-400"),
        create_yin_yang_svg('#ffa49f'),
        create_next_button(2),
        cls=page_classes
    )

@page.step(2)
async def step_2(request, form_data=None):
    viz_id = "yin_yang_visualization"
    viz_state = request.app.state.viz_state_manager.get_state(viz_id)
    
    return Div(
        *page.get_chunk_content(3),
        create_yin_yang_chart(
            generate_yin_yang_data(**viz_state.params) if viz_state.params else generate_yin_yang_data(),
            viz_id=viz_id,
            viz_state=viz_state.to_dict()
        ),
        create_form("?step=3", yin_class_color=("text", "What color represents the Yin class?", True)),
        cls=page_classes
    )

@page.step(3)
async def step_3(request, form_data=None):
    viz_id = "yin_yang_visualization"
    viz_state = request.app.state.viz_state_manager.get_state(viz_id)
    
    if form_data and 'yin_class_color' in form_data:
        user_answer = form_data['yin_class_color'].lower()
        if 'blue' in user_answer:
            request.app.state.viz_state_manager.update_state(viz_id, visible_controls=["n"])
            viz_state = request.app.state.viz_state_manager.get_state(viz_id)
            return Div(
                *page.get_chunk_content(4),
                create_yin_yang_chart(
                    generate_yin_yang_data(**viz_state.params) if viz_state.params else generate_yin_yang_data(),
                    viz_id=viz_id,
                    viz_state=viz_state.to_dict()
                ),
                create_form("?step=4", points_effect=("textarea", "Describe the effect of increasing the number of points:", True)),
                cls=page_classes
            )
        else:
            return Div(
                P("Not quite. Please try again.", cls="text-red-600 dark:text-red-400"),
                create_form("?step=3", yin_class_color=("text", "What color represents the Yin class?", True)),
                cls=page_classes
            )
    else:
        return Div(
            *page.get_chunk_content(3),
            create_yin_yang_chart(
                generate_yin_yang_data(**viz_state.params) if viz_state.params else generate_yin_yang_data(),
                viz_id=viz_id,
                viz_state=viz_state.to_dict()
            ),
            create_form("?step=3", yin_class_color=("text", "What color represents the Yin class?", True)),
            cls=page_classes
        )

@page.step(4)
async def step_4(request, form_data=None):
    viz_id = "yin_yang_visualization"
    viz_state = request.app.state.viz_state_manager.get_state(viz_id)
    
    if form_data and 'points_effect' in form_data:
        request.app.state.viz_state_manager.update_state(viz_id, visible_controls=["n", "r_small"])
        viz_state = request.app.state.viz_state_manager.get_state(viz_id)
        return Div(
            *page.get_chunk_content(5),
            create_yin_yang_chart(
                generate_yin_yang_data(**viz_state.params) if viz_state.params else generate_yin_yang_data(),
                viz_id=viz_id,
                viz_state=viz_state.to_dict()
            ),
            create_form("?step=5", small_radius_effect=("textarea", "Describe the effect of changing the small radius:", True)),
            cls=page_classes
        )
    else:
        return Div(
            *page.get_chunk_content(4),
            create_yin_yang_chart(
                generate_yin_yang_data(**viz_state.params) if viz_state.params else generate_yin_yang_data(),
                viz_id=viz_id,
                viz_state=viz_state.to_dict()
            ),
            create_form("?step=4", points_effect=("textarea", "Describe the effect of increasing the number of points:", True)),
            cls=page_classes
        )

@page.step(5)
async def step_5(request, form_data=None):
    viz_id = "yin_yang_visualization"
    viz_state = request.app.state.viz_state_manager.get_state(viz_id)
    
    if form_data and 'small_radius_effect' in form_data:
        request.app.state.viz_state_manager.update_state(viz_id, visible_controls=["n", "r_small", "r_big"])
        viz_state = request.app.state.viz_state_manager.get_state(viz_id)
        return Div(
            *page.get_chunk_content(6),
            create_yin_yang_chart(
                generate_yin_yang_data(**viz_state.params) if viz_state.params else generate_yin_yang_data(),
                viz_id=viz_id,
                viz_state=viz_state.to_dict()
            ),
            create_form("?step=6", big_radius_effect=("textarea", "Describe the effect of changing the big radius:", True)),
            cls=page_classes
        )
    else:
        return Div(
            *page.get_chunk_content(5),
            create_yin_yang_chart(
                generate_yin_yang_data(**viz_state.params) if viz_state.params else generate_yin_yang_data(),
                viz_id=viz_id,
                viz_state=viz_state.to_dict()
            ),
            create_form("?step=5", small_radius_effect=("textarea", "Describe the effect of changing the small radius:", True)),
            cls=page_classes
        )

@page.step(6)
async def step_6(request, form_data=None):
    viz_id = "yin_yang_visualization"
    viz_state = request.app.state.viz_state_manager.get_state(viz_id)
    
    if form_data and 'big_radius_effect' in form_data:
        return Div(
            *page.get_chunk_content(7),
            *page.get_chunk_content(8),
            create_page_navigation(request, page),
            cls=page_classes
        )
    else:
        return Div(
            *page.get_chunk_content(6),
            create_yin_yang_chart(
                generate_yin_yang_data(**viz_state.params) if viz_state.params else generate_yin_yang_data(),
                viz_id=viz_id,
                viz_state=viz_state.to_dict()
            ),
            create_form("?step=6", big_radius_effect=("textarea", "Describe the effect of changing the big radius:", True)),
            cls=page_classes
        )