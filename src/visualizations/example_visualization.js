// src/visualizations/example_visualization.js

if (typeof window.ExampleVisualization === 'undefined') {
    window.ExampleVisualization = class {
        constructor(vizId, params) {
            this.vizId = vizId;
            this.params = params;
        }

        drawVisualization(svg) {
            svg.append("circle")
                .attr("cx", 200)
                .attr("cy", 200)
                .attr("r", 100)
                .attr("fill", "blue");
        }
    };
}