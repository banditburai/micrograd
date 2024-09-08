from fasthtml.common import *
from utils import RNG, gen_data_yinyang
import json

random = RNG(42)

def generate_yin_yang_data(n=1000, r_small=0.1, r_big=0.5):
    train, val, test = gen_data_yinyang(random, n=n, r_small=r_small, r_big=r_big)
    all_data = train + val + test
    return [{"x": point[0][0], "y": point[0][1], "class": point[1]} for point in all_data]

def create_yin_yang_chart(data, size=600):
    return Div(
        Div(
            id="chart-svg-container",
            cls="w-full h-[600px] flex justify-center items-center",
        ),
        Script(f"""
        function createYinYangChart() {{
            const data = {json.dumps(data)};
            const container = document.getElementById('chart-svg-container');
            const containerSize = Math.min(container.clientWidth, container.clientHeight, {size});
            
            // Clear previous chart if any
            container.innerHTML = '';

            const margin = {{top: 20, right: 20, bottom: 50, left: 20}};
            const chartSize = containerSize - margin.top - margin.bottom;

            const svg = d3.select("#chart-svg-container")
                .append("svg")
                .attr("width", containerSize)
                .attr("height", containerSize)
                .append("g")
                .attr("transform", `translate(${{margin.left}},${{margin.top}})`);

            let zoomLevel = 1;
            const zoom = d3.zoom()
                .scaleExtent([0.5, 5])
                .on("zoom", zoomed)
                .filter(event => event.type === 'mousedown' ? false : true); // Disable dragging

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
                zoomLevel = event.transform.k;
                plotGroup.attr("transform", event.transform);
                updateDataPoints();
                sliderGroup.select("circle").attr("cx", zoomScale(zoomLevel));
            }}

            function updateDataPoints() {{
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
                .attr("r", 3)
                .attr("fill", d => colorScale(d.class));

            // Add hover circles
            const hoverCircles = plotGroup.selectAll("circle.hover-circle")
                .data(data)
                .join("circle")
                .attr("class", "hover-circle")
                .attr("cx", d => xScale(d.x))
                .attr("cy", d => yScale(d.y))
                .attr("r", 6)
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
                .attr("cx", zoomScale(1))
                .attr("fill", "var(--slider-handle-color)")
                .call(d3.drag()
                    .on("drag", (event) => {{
                        const newZoom = zoomScale.invert(event.x);
                        const newTransform = d3.zoomIdentity
                            .translate(chartSize / 2, chartSize / 2)
                            .scale(newZoom)
                            .translate(-chartSize / 2, -chartSize / 2);
                        svg.call(zoom.transform, newTransform);
                    }})
                );
        }}

        // Initial creation
        createYinYangChart();

        // Redraw on window resize
        window.addEventListener('resize', createYinYangChart);
        """),
        id="chart-container",
        cls="flex flex-col items-center w-full max-w-3xl mx-auto",
    )