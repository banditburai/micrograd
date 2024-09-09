from fasthtml.common import *
import json
from utils import RNG, gen_data_yinyang

random = RNG(42)

def generate_yin_yang_data(n=1000, r_small=0.1, r_big=0.5):
    train, val, test = gen_data_yinyang(random, n=n, r_small=r_small, r_big=r_big)
    all_data = train + val + test
    return [{"x": point[0][0], "y": point[0][1], "class": point[1]} for point in all_data]

def create_yin_yang_chart(data, size=600, viz_id="yin_yang", viz_state=None):        
    if viz_state is None:
        viz_state = {"zoom_level": 1.0, "visible_controls": [], "params": {}}

    controls = Div(
        Div(
            Label("Number of points: ", Span(f"{viz_state['params'].get('n', 1000)}", id=f"{viz_id}-n-value")),
            Input(type="range", name="n", value=f"{viz_state['params'].get('n', 1000)}", min="100", max="5000", step="100",
                  oninput=f"document.getElementById('{viz_id}-n-value').textContent = this.value",
                  hx_post="/update_yin_yang",
                  hx_target=f"#{viz_id}-container",
                  hx_trigger="change",
                  hx_vals=f'js:{{"{viz_id}": "{viz_id}", "zoom_level": zoomLevel}}'),
            cls="mt-2 flex items-center space-x-2",
            style="display: inline-block" if "n" in viz_state["visible_controls"] else "display: none"
        ),
        Div(
            Label("Small radius: ", Span(f"{viz_state['params'].get('r_small', 0.1)}", id=f"{viz_id}-r-small-value")),
            Input(type="range", name="r_small", value=f"{viz_state['params'].get('r_small', 0.1)}", min="0.01", max="0.5", step="0.01",
                  oninput=f"document.getElementById('{viz_id}-r-small-value').textContent = this.value",
                  hx_post="/update_yin_yang",
                  hx_target=f"#{viz_id}-container",
                  hx_trigger="change",
                  hx_vals=f'js:{{"{viz_id}": "{viz_id}", "zoom_level": zoomLevel}}'),
            cls="mt-2 flex items-center space-x-2",
            style="display: inline-block" if "r_small" in viz_state["visible_controls"] else "display: none"
        ),
        Div(
            Label("Big radius: ", Span(f"{viz_state['params'].get('r_big', 0.5)}", id=f"{viz_id}-r-big-value")),
            Input(type="range", name="r_big", value=f"{viz_state['params'].get('r_big', 0.5)}", min="0.1", max="1.0", step="0.01",
                  oninput=f"document.getElementById('{viz_id}-r-big-value').textContent = this.value",
                  hx_post="/update_yin_yang",
                  hx_target=f"#{viz_id}-container",
                  hx_trigger="change",
                  hx_vals=f'js:{{"{viz_id}": "{viz_id}", "zoom_level": zoomLevel}}'),
            cls="mt-2 flex items-center space-x-2",
            style="display: inline-block" if "r_big" in viz_state["visible_controls"] else "display: none"
        ),
        cls="space-y-4"
    )

    return Div(
        Div(
            id=f"{viz_id}-svg-container",
            cls="w-full h-[600px] flex justify-center items-center",
        ),
        controls,
        Script(f"""
        console.log('Initializing chart with viz_state:', {json.dumps(viz_state)});
        var zoomLevel = {viz_state['zoom_level']};
        console.log('Initial zoomLevel:', zoomLevel);
        
        function createYinYangChart() {{
            console.log('Creating chart with zoomLevel:', zoomLevel);
            const data = {json.dumps(data)};
            const container = document.getElementById('{viz_id}-svg-container');
            const containerSize = Math.min(container.clientWidth, container.clientHeight, {size});
            
            // Clear previous chart if any
            container.innerHTML = '';

            const margin = {{top: 20, right: 20, bottom: 50, left: 20}};
            const chartSize = containerSize - margin.top - margin.bottom;

            const svg = d3.select("#{viz_id}-svg-container")
                .append("svg")
                .attr("width", containerSize)
                .attr("height", containerSize)
                .append("g")
                .attr("transform", `translate(${{margin.left}},${{margin.top}})`);

            const zoom = d3.zoom()
                .scaleExtent([0.5, 5])
                .on("zoom", zoomed)
                .filter(event => event.type === 'mousedown' ? false : true);

            svg.call(zoom);

            const xScale = d3.scaleLinear()
                .domain([-1, 1])
                .range([0, chartSize]);

            const yScale = d3.scaleLinear()
                .domain([-1, 1])
                .range([chartSize, 0]);

            const colorScale = d3.scaleOrdinal()
                .domain([0, 1, 2])
                .range(["#1f77b4", "#ff7f0e", "#2ca02c"]);

            // Add subtle grid
            const grid = svg.append("g")
                .attr("class", "grid")
                .attr("opacity", 0.1);

            grid.append("g")
                .attr("transform", `translate(0,${{chartSize}})`)
                .call(d3.axisBottom(xScale).tickSize(-chartSize).tickFormat(""));

            grid.append("g")
                .call(d3.axisLeft(yScale).tickSize(-chartSize).tickFormat(""));

            const plotGroup = svg.append("g");

            function zoomed(event) {{
                console.log('Zoom event:', event.transform.k);
                zoomLevel = event.transform.k;
                
                // Apply zoom and translation to keep the chart centered
                plotGroup.attr("transform", `translate(${{event.transform.x + margin.left}}, ${{event.transform.y + margin.top}}) scale(${{event.transform.k}})`);
                
                updateDataPoints();
                sliderHandle.attr("cx", zoomScale(zoomLevel));
            }}

            function updateDataPoints() {{
                console.log('Updating data points with zoomLevel:', zoomLevel);
                dataPoints.attr("r", 3 / zoomLevel);
                hoverCircles.attr("r", 6 / zoomLevel);
            }}

            // Draw data points
            const dataPoints = plotGroup.selectAll("circle.data-point")
                .data(data)
                .join("circle")
                .attr("class", "data-point")
                .attr("cx", d => xScale(d.x))
                .attr("cy", d => yScale(d.y))
                .attr("r", 3 / zoomLevel)
                .attr("fill", d => colorScale(d.class));    
            
                                
            // Add hover circles
            const hoverCircles = plotGroup.selectAll("circle.hover-circle")
                .data(data)
                .join("circle")
                .attr("class", "hover-circle")
                .attr("cx", d => xScale(d.x))
                .attr("cy", d => yScale(d.y))
                .attr("r", 6 / zoomLevel)
                .attr("fill", "none")
                .attr("stroke", "var(--stroke-color)")
                .attr("stroke-width", 1)
                .attr("opacity", 0);

            // Add fixed tooltip
            const tooltip = svg.append("g")
                .attr("class", "tooltip")
                .attr("transform", `translate(${{chartSize - 120}}, ${{chartSize - 50}})`)
                .attr("opacity", 0);

            tooltip.append("rect")
                .attr("width", 100)
                .attr("height", 40)
                .attr("fill", "var(--bg-color)")
                .attr("stroke", "var(--stroke-color)")
                .attr("stroke-width", 1)
                .attr("rx", 5);

            const tooltipX = tooltip.append("text")
                .attr("x", 10)
                .attr("y", 15)
                .attr("fill", "var(--text-color)");

            const tooltipY = tooltip.append("text")
                .attr("x", 10)
                .attr("y", 35)
                .attr("fill", "var(--text-color)");

            // Add hover effect
            dataPoints.on("mouseover", function(event, d) {{
                d3.select(this).attr("r", 4 / zoomLevel);
                const hoverCircle = d3.select(this.parentNode).select(`circle.hover-circle[cx="${{this.getAttribute('cx')}}"][cy="${{this.getAttribute('cy')}}"]`);
                hoverCircle
                    .attr("opacity", 1)
                    .attr("r", 8 / zoomLevel);
                tooltip.attr("opacity", 1);
                tooltipX.text(`X: ${{d.x.toFixed(2)}}`);
                tooltipY.text(`Y: ${{d.y.toFixed(2)}}`);
            }})
            .on("mouseout", function() {{
                d3.select(this).attr("r", 3 / zoomLevel);
                const hoverCircle = d3.select(this.parentNode).select(`circle.hover-circle[cx="${{this.getAttribute('cx')}}"][cy="${{this.getAttribute('cy')}}"]`);
                hoverCircle
                    .attr("opacity", 0)
                    .attr("r", 6 / zoomLevel);
                tooltip.attr("opacity", 0);
            }});

            // Add legend
            const legend = svg.append("g")
                .attr("class", "legend")
                .attr("transform", `translate(${{chartSize - 100}}, 20)`);

            ["Yin", "Yang", "Boundary"].forEach((label, i) => {{
                const legendItem = legend.append("g")
                    .attr("transform", `translate(0, ${{i * 20}})`);

                legendItem.append("circle")
                    .attr("cx", 0)
                    .attr("cy", 0)
                    .attr("r", 6)
                    .attr("fill", colorScale(i));

                legendItem.append("text")
                    .attr("x", 15)
                    .attr("y", 0)
                    .attr("dy", "0.32em")
                    .attr("fill", "var(--text-color)")
                    .text(label);
            }});

            // Add zoom slider
            const sliderWidth = chartSize * 0.8;
            const zoomScale = d3.scaleLinear()
                .domain([0.5, 5])
                .range([0, sliderWidth])
                .clamp(true);

            const sliderGroup = svg.append("g")
                .attr("class", "slider")
                .attr("transform", `translate(${{(chartSize - sliderWidth) / 2}},${{chartSize + 20}})`);

            sliderGroup.append("line")
                .attr("class", "track")
                .attr("x1", zoomScale.range()[0])
                .attr("x2", zoomScale.range()[1])
                .attr("stroke", "var(--slider-track-color)")
                .attr("stroke-width", 10)
                .attr("stroke-linecap", "round");

            const sliderHandle = sliderGroup.append("circle")
                .attr("class", "handle")
                .attr("r", 8)
                .attr("cx", zoomScale(zoomLevel))
                .attr("fill", "var(--slider-handle-color)")
                .call(d3.drag()
                    .on("drag", (event) => {{
                        const newZoom = zoomScale.invert(event.x);
                        console.log('Slider dragged, new zoom:', newZoom);
                        const newTransform = d3.zoomIdentity
                            .translate(chartSize / 2, chartSize / 2)
                            .scale(newZoom)
                            .translate(-chartSize / 2, -chartSize / 2);
                        svg.call(zoom.transform, newTransform);
                    }})
                );

            // Update zoom at the end of createYinYangChart
            console.log('Applying initial zoom:', zoomLevel);
            const initialTransform = d3.zoomIdentity
                .translate(chartSize / 2, chartSize / 2)
                .scale(zoomLevel)
                .translate(-chartSize / 2, -chartSize / 2);
            svg.call(zoom.transform, initialTransform);

        }}

        // Initial creation
        createYinYangChart();

        // Redraw on window resize
        window.addEventListener('resize', createYinYangChart);
        """),
        id=f"{viz_id}-container",
        cls="flex flex-col items-center w-full max-w-3xl mx-auto",
    )