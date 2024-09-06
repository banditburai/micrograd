from fasthtml.common import *
from micrograd import Value, MLP, AdamW, cross_entropy
from utils import RNG, gen_data_yinyang, trace
import json
import numpy as np

app, rt = fast_app(
    hdrs=[
        Script(src="https://cdn.jsdelivr.net/npm/d3@7"),
    ]
)

# Global variables
random = RNG(42)
model = MLP(2, [8, 3])
optimizer = AdamW(model.parameters(), lr=1e-1, weight_decay=1e-4)
train_split, val_split, test_split = gen_data_yinyang(random, n=100)
step = 0
num_steps = 100

def loss_fun(model, split):
    total_loss = Value(0.0)
    for x, y in split:
        logits = model([Value(x[0]), Value(x[1])])
        loss = cross_entropy(logits, y)
        total_loss = total_loss + loss
    mean_loss = total_loss * (1.0 / len(split))
    return mean_loss

@rt('/')
def get():
    return Titled("MicroGrad Visualization",
        Div(
            Div(id="decision-boundary"),
            Div(id="computational-graph"),
            Div(id="optimizer-state"),
            Div(
                Button("Reset", id="reset-btn", hx_post="/reset", hx_target="#control-panel"),
                Button("Play/Pause", id="toggle-btn", hx_post="/toggle_training", hx_target="#control-panel"),
                Button("Step", id="step-btn", hx_post="/train_step", hx_target="#control-panel"),
                Input(type="number", id="learning-rate", value="0.1", step="0.01"),
                CheckboxX(id="show-level-sets", label="Show level sets"),
                id="control-panel"
            )
        ),
        Script(init_visualizations(), type="module")
    )

def init_visualizations():
    return """
    document.addEventListener('DOMContentLoaded', function() {
        initDecisionBoundary();
        initComputationalGraph();
        initOptimizerState();
        
        // Initial data fetch
        fetch('/initial_data')
            .then(response => response.json())
            .then(data => {
                updateDecisionBoundary(data.decision_boundary);
                updateComputationalGraph(data.computational_graph);
                updateOptimizerState(data.optimizer_state);
            });
    });
    
    function initDecisionBoundary() {
        const width = 500;
        const height = 500;
        const margin = {top: 20, right: 20, bottom: 30, left: 40};
        
        const svg = d3.select("#decision-boundary")
            .append("svg")
            .attr("width", width + margin.left + margin.right)
            .attr("height", height + margin.top + margin.bottom)
            .append("g")
            .attr("transform", `translate(${margin.left},${margin.top})`);
        
        // Add axes here if needed
    }
    
    function initComputationalGraph() {
        const width = 600;
        const height = 400;
        
        d3.select("#computational-graph")
            .append("svg")
            .attr("width", width)
            .attr("height", height)
            .append("g")
            .attr("transform", "translate(40,20)");
    }
    
    function initOptimizerState() {
        d3.select("#optimizer-state").append("table");
    }
    
    function updateDecisionBoundary(data) {
        const svg = d3.select("#decision-boundary svg g");
        const width = 500;
        const height = 500;
        
        const x = d3.scaleLinear().domain([-2, 2]).range([0, width]);
        const y = d3.scaleLinear().domain([-2, 2]).range([height, 0]);
        
        const color = d3.scaleOrdinal()
            .domain([0, 1, 2])
            .range(["#ff0000", "#00ff00", "#0000ff"]);
        
        svg.selectAll("*").remove();
        
        svg.selectAll("rect")
            .data(data.z.flat())
            .enter()
            .append("rect")
            .attr("x", (d, i) => x(data.x.flat()[i]))
            .attr("y", (d, i) => y(data.y.flat()[i]))
            .attr("width", width / 100)
            .attr("height", height / 100)
            .attr("fill", d => color(d))
            .attr("opacity", 0.5);
        
        svg.selectAll("circle")
            .data(data.train_data)
            .enter()
            .append("circle")
            .attr("cx", d => x(d[0]))
            .attr("cy", d => y(d[1]))
            .attr("r", 3)
            .attr("fill", d => color(d[2]))
            .attr("stroke", "black");
    }
    
    function updateComputationalGraph(data) {
        const svg = d3.select("#computational-graph svg g");
        const width = 520;
        const height = 360;

        const simulation = d3.forceSimulation(data.nodes)
            .force("link", d3.forceLink(data.links).id(d => d.id))
            .force("charge", d3.forceManyBody().strength(-50))
            .force("center", d3.forceCenter(width / 2, height / 2));

        const link = svg.selectAll(".link")
            .data(data.links)
            .join("line")
            .attr("class", "link")
            .attr("stroke", "#999")
            .attr("stroke-opacity", 0.6);

        const node = svg.selectAll(".node")
            .data(data.nodes)
            .join("g")
            .attr("class", "node")
            .call(d3.drag()
                .on("start", dragstarted)
                .on("drag", dragged)
                .on("end", dragended));

        node.append("circle")
            .attr("r", 5)
            .attr("fill", "#69b3a2");

        node.append("text")
            .attr("dx", 12)
            .attr("dy", ".35em")
            .text(d => `${d.op}\\ndata: ${d.data.toFixed(4)}\\ngrad: ${d.grad.toFixed(4)}`)
            .attr("font-size", "10px");

        simulation.on("tick", () => {
            link
                .attr("x1", d => d.source.x)
                .attr("y1", d => d.source.y)
                .attr("x2", d => d.target.x)
                .attr("y2", d => d.target.y);

            node
                .attr("transform", d => `translate(${d.x},${d.y})`);
        });

        function dragstarted(event) {
            if (!event.active) simulation.alphaTarget(0.3).restart();
            event.subject.fx = event.subject.x;
            event.subject.fy = event.subject.y;
        }

        function dragged(event) {
            event.subject.fx = event.x;
            event.subject.fy = event.y;
        }

        function dragended(event) {
            if (!event.active) simulation.alphaTarget(0);
            event.subject.fx = null;
            event.subject.fy = null;
        }
    }
    
    function updateOptimizerState(data) {
        const table = d3.select("#optimizer-state table");
        
        if (table.select("thead").empty()) {
            table.append("thead").append("tr")
                .selectAll("th")
                .data(["Param", "Value", "Grad", "m", "v"])
                .enter()
                .append("th")
                .text(d => d);
        }
        
        const rows = table.select("tbody").selectAll("tr")
            .data(data);
        
        rows.enter()
            .append("tr")
            .merge(rows)
            .html(d => `
                <td>${d.param}</td>
                <td>${d.value.toFixed(4)}</td>
                <td>${d.grad.toFixed(4)}</td>
                <td>${d.m.toFixed(4)}</td>
                <td>${d.v.toFixed(4)}</td>
            `);
        
        rows.exit().remove();
    }
    """

@rt('/initial_data')
def get():
    return json.dumps({
        'decision_boundary': get_decision_boundary_data(),
        'computational_graph': get_computational_graph_data(),
        'optimizer_state': get_optimizer_state_data()
    })

@rt('/train_step')
def post():
    global step
    if step < num_steps:
        step += 1
        loss = loss_fun(model, train_split)
        loss.backward()
        optimizer.step()
        optimizer.zero_grad()
        
        return json.dumps({
            'decision_boundary': get_decision_boundary_data(),
            'computational_graph': get_computational_graph_data(),
            'optimizer_state': get_optimizer_state_data()
        })
    return "Training complete"

def get_decision_boundary_data():
    x = np.linspace(-2, 2, 100)
    y = np.linspace(-2, 2, 100)
    X, Y = np.meshgrid(x, y)
    Z = np.zeros_like(X)
    
    for i in range(X.shape[0]):
        for j in range(X.shape[1]):
            logits = model([Value(X[i, j]), Value(Y[i, j])])
            Z[i, j] = np.argmax([l.data for l in logits])
    
    return {
        'x': X.tolist(),
        'y': Y.tolist(),
        'z': Z.tolist(),
        'train_data': [[x[0], x[1], y] for x, y in train_split]
    }

def get_computational_graph_data():
    loss = loss_fun(model, train_split[:1])  # Use only the first training example
    loss.backward()
    nodes, edges = trace(loss)
    
    return {
        'nodes': [{'id': id(n), 'op': n._op, 'data': n.data, 'grad': n.grad} for n in nodes],
        'links': [{'source': id(n1), 'target': id(n2)} for n1, n2 in edges]
    }

def get_optimizer_state_data():
    data = []
    for i, p in enumerate(model.parameters()):
        data.append({
            'param': i,
            'value': p.data,
            'grad': p.grad,
            'm': p.m,
            'v': p.v
        })
    return data

@rt('/reset')
def post():
    global model, optimizer, step
    model = MLP(2, [8, 3])
    optimizer = AdamW(model.parameters(), lr=1e-1, weight_decay=1e-4)
    step = 0
    return json.dumps({
        'decision_boundary': get_decision_boundary_data(),
        'computational_graph': get_computational_graph_data(),
        'optimizer_state': get_optimizer_state_data()
    })

@rt('/toggle_training')
def post():
    # This function will be called when the Play/Pause button is clicked
    # implement the logic to start/stop the training loop here
    pass

if __name__ == "__main__":
    import sys
    if sys.argv[0].endswith("_mp_fork_launch"):
        # This is the child process, do nothing
        pass
    else:
        # This is the parent process, run the server
        serve()