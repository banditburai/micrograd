from fasthtml.common import *
from utils import RNG, gen_data_yinyang
import json

app, rt = fast_app(
    hdrs=[
        Script(src="https://cdn.jsdelivr.net/npm/d3@7"),
    ]
)

random = RNG(42)

def generate_yin_yang_data(n=1000, r_small=0.1, r_big=0.5):
    train, val, test = gen_data_yinyang(random, n=n, r_small=r_small, r_big=r_big)
    all_data = train + val + test
    return [{"x": point[0][0], "y": point[0][1], "class": point[1]} for point in all_data]

def create_chart(data):
    return Div(
        Script(f"""
        (function() {{
            const data = {json.dumps(data)};
            const width = 600;
            const height = 600;
            const margin = {{top: 20, right: 120, bottom: 20, left: 20}};

            const svg = d3.select("#chart")
                .append("svg")
                .attr("width", width + margin.left + margin.right)
                .attr("height", height + margin.top + margin.bottom)
                .append("g")
                .attr("transform", `translate(${{margin.left}},${{margin.top}})`);

            const xScale = d3.scaleLinear()
                .domain([-1, 1])
                .range([0, width]);

            const yScale = d3.scaleLinear()
                .domain([-1, 1])
                .range([height, 0]);

            const colorScale = d3.scaleOrdinal()
                .domain([0, 1, 2])
                .range(["#1f77b4", "#ff7f0e", "#2ca02c"]);


            // Draw data points
            svg.selectAll("circle.data-point")
                .data(data)
                .join("circle")
                .attr("class", "data-point")
                .attr("cx", d => xScale(d.x))
                .attr("cy", d => yScale(d.y))
                .attr("r", 3)
                .attr("fill", d => colorScale(d.class));

            // Add legend
            const legend = svg.append("g")
                .attr("transform", `translate(${{width + 20}}, 0)`);

            ["Yin", "Yang", "Boundary"].forEach((label, i) => {{
                const legendItem = legend.append("g")
                    .attr("transform", `translate(0, ${{i * 25}})`);

                legendItem.append("circle")
                    .attr("cx", 0)
                    .attr("cy", 0)
                    .attr("r", 6)
                    .attr("fill", colorScale(i));

                legendItem.append("text")
                    .attr("x", 15)
                    .attr("y", 0)
                    .attr("dy", "0.35em")
                    .text(label)
                    .attr("fill", "#888");  // Light gray text for better visibility in dark mode
            }});
        }})();
        """),
        id="chart"
    )

@rt('/')
def get():
    initial_data = generate_yin_yang_data()
    return Titled("Yin Yang Dataset Visualization",
        Div(
            Form(
                Div(
                    Label("Number of points: ", Span("1000", id="n-value")),
                    Input(type="range", name="n", value="1000", min="100", max="5000", step="100",
                          oninput="document.getElementById('n-value').textContent = this.value"),
                ),
                Div(
                    Label("Small radius: ", Span("0.1", id="r-small-value")),
                    Input(type="range", name="r_small", value="0.1", min="0.01", max="0.5", step="0.01",
                          oninput="document.getElementById('r-small-value').textContent = this.value"),
                ),
                Div(
                    Label("Big radius: ", Span("0.5", id="r-big-value")),
                    Input(type="range", name="r_big", value="0.5", min="0.1", max="1.0", step="0.01",
                          oninput="document.getElementById('r-big-value').textContent = this.value"),
                ),
                Button("Generate", type="submit"),
                hx_post="/generate",
                hx_target="#chart",
                hx_swap="outerHTML",
                hx_trigger="change, submit"
            ),
            create_chart(initial_data)
        )
    )

@rt('/generate')
def post(n: int = 1000, r_small: float = 0.1, r_big: float = 0.5):
    new_data = generate_yin_yang_data(n, r_small, r_big)
    return create_chart(new_data)

serve()