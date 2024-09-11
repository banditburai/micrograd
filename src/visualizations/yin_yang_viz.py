from fasthtml.common import *
import json

def create_chart_script(size, viz_id, viz_state):
    return Script(f"""
        console.log('Initializing chart with viz_state:', {json.dumps(viz_state)});
        var zoomLevel = {viz_state['zoom_level']};        
        
        function createYinYangChart() {{
            const n = {viz_state['params']['n']};
            const rSmall = {viz_state['params']['r_small']};
            const rBig = {viz_state['params']['r_big']};

            // Generate data on the client side
            const dataObj = genDataYinYang(random, n, rSmall, rBig);
            const data = dataObj.train;  // Use the training data for visualization
            const container = document.getElementById('{viz_id}-svg-container');
            const containerSize = Math.min(container.clientWidth, container.clientHeight);
            
            // Clear previous chart
            container.innerHTML = '';

            const margin = {{top: 20, right: 20, bottom: 50, left: 40}};
            const width = containerSize - margin.left - margin.right;
            const height = containerSize - margin.top - margin.bottom;

            const svg = d3.select(container)
                .append("svg")
                .attr("width", "100%")
                .attr("height", "100%")
                .attr("viewBox", `0 0 ${{containerSize}} ${{containerSize}}`)
                .attr("preserveAspectRatio", "xMidYMid meet");

            // Scales
            const xScale = d3.scaleLinear().domain([-1, 1]).range([0, width]);
            const yScale = d3.scaleLinear().domain([-1, 1]).range([height, 0]);
            const colorScale = d3.scaleOrdinal()
                .domain([0, 1, 2])
                .range(["#1f77b4", "#ff7f0e", "#2ca02c"]);

            // Draw points
            svg.selectAll("circle")
                .data(data)
                .enter()
                .append("circle")
                .attr("cx", d => xScale(d[0][0]))  // Accessing x coordinate
                .attr("cy", d => yScale(d[0][1]))  // Accessing y coordinate
                .attr("r", 3)
                .attr("fill", d => colorScale(d[1]));  // Accessing class

            // Add axes
            svg.append("g")
                .attr("transform", `translate(0,${{height}})`)
                .call(d3.axisBottom(xScale));

            svg.append("g")
                .call(d3.axisLeft(yScale));
        }}

        // Initial creation
        createYinYangChart();

        // Redraw on window resize
        window.addEventListener('resize', createYinYangChart);
    """)

def create_d3_sliders(viz_id, params):
    sliders = [
        {"id": "n", "min": 100, "max": 5000, "step": 100, "value": params['n'], "label": "Number of points"},
        {"id": "r_small", "min": 0.01, "max": 0.5, "step": 0.01, "value": params['r_small'], "label": "Small radius"},
        {"id": "r_big", "min": 0.1, "max": 1.0, "step": 0.01, "value": params['r_big'], "label": "Big radius"},
    ]

    slider_html = ""
    for slider in sliders:
        slider_html += f"""
            <div class="slider-container">
                <label for="{slider['id']}">{slider['label']}: <span id="{slider['id']}-value">{slider['value']}</span></label>
                <input type="range" id="{slider['id']}" min="{slider['min']}" max="{slider['max']}" step="{slider['step']}" value="{slider['value']}">
            </div>
        """

    return Div(
        Div(slider_html, cls="d3-slider-container"),
        cls="flex flex-col space-y-4"
    )

def create_yin_yang_chart(size=600, viz_id="yin_yang", viz_state=None):        
    if viz_state is None:
        viz_state = {"zoom_level": 1.0, "visible_controls": [], "params": {"n": 1000, "r_small": 0.1, "r_big": 0.5}}  # Set default params here
    
    # Ensure params have default values
    params = viz_state.get('params', {"n": 1000, "r_small": 0.1, "r_big": 0.5})  # Provide defaults if not present

    # Create sliders
    sliders = create_d3_sliders(viz_id, params)

    return Div(
        Div(
            id=f"{viz_id}-svg-container",
            cls="w-full h-[600px] flex justify-center items-center border-2 border-red-500 min-h-[300px]",
        ),
        sliders,
        create_chart_script(size, viz_id, viz_state),
        id=f"{viz_id}-container",
        cls="flex flex-col items-center w-full max-w-3xl mx-auto",
    )