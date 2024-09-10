class YinYangChart extends HTMLElement {
    constructor() {
        super();
        this.attachShadow({ mode: 'open' });
    }

    connectedCallback() {
        this.render();
        this.initChart();
    }

    render() {
        this.shadowRoot.innerHTML = `
            <div id="chart-container" class="w-full h-[400px]"></div>
            <div id="controls" class="w-full mt-4"></div>
        `;
    }

    initChart() {
        const vizId = this.getAttribute('viz-id');
        const params = JSON.parse(this.getAttribute('params'));

        console.log('Initializing chart with ID:', vizId);
        console.log('Parameters:', params);

        // Function to initialize the chart
        const initialize = () => {
            if (typeof createYinYangChart === 'function') {
                createYinYangChart(vizId, params);
            } else {
                setTimeout(initialize, 100); // Retry after 100ms
            }
        };

        // Check if the document is still loading
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', initialize);
        } else {
            initialize(); // Document is already loaded
        }
    }

    updateChart(params) {
        const vizId = this.getAttribute('viz-id');
        createYinYangChart(vizId, params);
    }
}

function createYinYangChart(containerId, params) {
    const width = 400;
    const height = 400;
    const margin = { top: 20, right: 20, bottom: 50, left: 40 };

    const svg = d3.select(`#${containerId}`)
        .append("svg")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)
        .append("g")
        .attr("transform", `translate(${margin.left},${margin.top})`);

    function updateChart() {
        // Clear previous content
        svg.selectAll("*").remove();

        // Generate data
        const data = generateData(params.n, params.r_small, params.r_big);

        // Set up scales
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
            .attr("cx", d => xScale(d.x))
            .attr("cy", d => yScale(d.y))
            .attr("r", 3)
            .attr("fill", d => colorScale(d.class));

        // Add axes
        svg.append("g")
            .attr("transform", `translate(0,${height})`)
            .call(d3.axisBottom(xScale));

        svg.append("g")
            .call(d3.axisLeft(yScale));
    }

    function generateData(n, r_small, r_big) {
        const data = [];
        for (let i = 0; i < n; i++) {
            const x = Math.random() * 2 - 1;
            const y = Math.random() * 2 - 1;
            const d = Math.sqrt(x*x + y*y);
            let cls;
            if (d < r_small) cls = 2;
            else if (y > 0) cls = 0;
            else cls = 1;
            data.push({x, y, class: cls});
        }
        return data;
    }

    // Create sliders
    const sliders = [
        {id: "n", min: 100, max: 5000, step: 100, value: params.n, label: "Number of points"},
        {id: "r_small", min: 0.01, max: 0.5, step: 0.01, value: params.r_small, label: "Small radius"},
        {id: "r_big", min: 0.1, max: 1, step: 0.01, value: params.r_big, label: "Big radius"}
    ];

    sliders.forEach(slider => {
        d3.select(`#${containerId}-controls`)
            .append("div")
            .attr("class", "slider-container")
            .html(`
                <label for="${slider.id}">${slider.label}: <span id="${slider.id}-value">${slider.value}</span></label>
                <input type="range" id="${slider.id}" min="${slider.min}" max="${slider.max}" step="${slider.step}" value="${slider.value}">
            `);

        d3.select(`#${slider.id}`).on("input", function() {
            const value = +this.value;
            d3.select(`#${slider.id}-value`).text(value);
            params[slider.id] = value;
            updateChart();
        });
    });

    updateChart();
}

customElements.define('yin-yang-chart', YinYangChart);