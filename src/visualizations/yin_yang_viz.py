from fasthtml.common import *
import json

def create_yin_yang_chart(viz_id, viz_state):
    params_json = json.dumps(viz_state['params'])
    return Div(
        f'<yin-yang-chart viz-id="{viz_id}" params=\'{params_json}\'></yin-yang-chart>',  # Use the Web Component
        id=f"{viz_id}-wrapper",
        cls="w-full max-w-3xl mx-auto",
    )

def update_yin_yang_chart(viz_id, viz_state):
    return Script(f"""
        if (typeof createYinYangChart === 'function') {{
            createYinYangChart('{viz_id}', {json.dumps(viz_state['params'])});
        }}
    """)