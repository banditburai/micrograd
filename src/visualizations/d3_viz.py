from fasthtml.common import Div, Script
import json
import os

class D3Visualization:
    def __init__(self, viz_id, params):
        self.viz_id = viz_id
        self.params = params

    def create_container(self):
        return Div(
            Div(id=f"{self.viz_id}-svg-container", cls="w-full h-[400px] border border-gray-300"),
            id=f"{self.viz_id}-container",
            cls="flex flex-col items-center"
        )

    def create_chart_script(self, js_file):
        # Extract the base name from the js_file
        base_name = os.path.splitext(os.path.basename(js_file))[0]
        class_name = base_name.split('_')[0].capitalize() + "Visualization"  # Get the first part before the underscore

        return Script(f"""
            (function() {{
                // Clear previous content
                const container = document.getElementById('{self.viz_id}-svg-container');
                container.innerHTML = '';  // Clear previous content

                const svg = d3.select(container)
                    .append("svg")
                    .attr("width", "100%")
                    .attr("height", "100%");

                // Load the specific visualization logic from the external JS file
                const script = document.createElement('script');
                script.src = '/src/visualizations/{js_file}';  // Adjust the path as necessary
                script.onload = function() {{
                    // Now that the script is loaded, we can safely create an instance of the visualization
                    const vizClass = window['{class_name}'];  // Access the class dynamically using string
                    if (typeof vizClass !== 'undefined') {{
                        const viz = new vizClass('{self.viz_id}', {json.dumps(self.params)});
                        viz.drawVisualization(svg);
                    }} else {{
                        console.error('{class_name} is not defined.');
                    }}
                }};
                document.head.appendChild(script);
            }})();
        """)

    def render(self, js_file):
        container = self.create_container()
        chart_script = self.create_chart_script(js_file)
        return Div(container, chart_script)