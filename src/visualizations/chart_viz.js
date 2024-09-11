// src/visualizations/chart_viz.js

if (typeof window.ChartVisualization === 'undefined') {
    window.ChartVisualization = class {
        constructor(containerId, params) {
            this.containerId = containerId;
            this.params = params;
        }

        drawVisualization(svg) {
            const width = 400;
            const height = 400;

            // Generate sample data based on the number of points specified in params
            const data = Array.from({ length: this.params.n }, (_, i) => ({
                x: Math.random() * width,
                y: Math.random() * height
            }));

            // Draw points
            svg.selectAll("circle")
                .data(data)
                .enter()
                .append("circle")
                .attr("cx", d => d.x)
                .attr("cy", d => d.y)
                .attr("r", this.params.radius)  // Use the radius from params
                .attr("fill", this.params.color);  // Use the color from params
        }
    };
}