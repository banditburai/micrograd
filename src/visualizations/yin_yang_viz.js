// Wrap the entire content in an IIFE and expose createYinYangChart globally
(function(global) {
    function createYinYangChart(containerId, initialData, initialParams, visibleControls) {
        let data = initialData;
        let params = initialParams;
        let zoomLevel = params.zoom_level || 1;
        visibleControls = visibleControls || ['zoom'];  // Ensure zoom is always included

        const containerSize = Math.min(600, window.innerWidth - 40);
        const margin = {top: 0, right: 0, bottom: 50, left: 0};
        const chartSize = containerSize - margin.top - margin.bottom;

        const svg = d3.select(`#${containerId}`)
            .append("svg")
            .attr("width", containerSize)
            .attr("height", containerSize);

        const chartGroup = svg.append("g")
            .attr("transform", `translate(${margin.left},${margin.top})`);

        const xScale = d3.scaleLinear()
            .domain([-1, 1])
            .range([0, chartSize]);

        const yScale = d3.scaleLinear()
            .domain([-1, 1])
            .range([chartSize, 0]);

        const colorScale = d3.scaleOrdinal()
            .domain([0, 1, 2])
            .range(["#1f77b4", "#ff7f0e", "#2ca02c"]);

        const zoom = d3.zoom()
            .scaleExtent([0.5, 2])
            .on("zoom", zoomed)
            .filter(event => event.type === 'mousedown' ? false : true);

        chartGroup.call(zoom);

        // Add subtle grid
        const grid = chartGroup.append("g")
            .attr("class", "grid")
            .attr("opacity", 0.1);

        grid.append("g")
            .attr("transform", `translate(0,${chartSize})`)
            .call(d3.axisBottom(xScale)
                .ticks(10)
                .tickSize(-chartSize)
                .tickFormat("")
            );

        grid.append("g")
            .call(d3.axisLeft(yScale)
                .ticks(10)
                .tickSize(-chartSize)
                .tickFormat("")
            );

        const plotGroup = chartGroup.append("g");

        function zoomed(event) {
            zoomLevel = event.transform.k;
            plotGroup.attr("transform", event.transform);
            updateDataPoints();
            updateZoomSlider(zoomLevel);
        }

        function updateDataPoints() {
            dataPoints.attr("r", 3 / zoomLevel);
            hoverCircles.attr("r", 6 / zoomLevel);
        }

        let dataPoints, hoverCircles;

        function updateChart() {
            // Clear previous points
            plotGroup.selectAll("circle").remove();

            // Draw data points
            dataPoints = plotGroup.selectAll("circle.data-point")
                .data(data)
                .join("circle")
                .attr("class", "data-point")
                .attr("cx", d => xScale(d.x))
                .attr("cy", d => yScale(d.y))
                .attr("r", 3 / zoomLevel)
                .attr("fill", d => colorScale(d.class));

            // Add hover circles
            hoverCircles = plotGroup.selectAll("circle.hover-circle")
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

            // Add hover effect
            dataPoints.on("mouseover", function(event, d) {
                d3.select(this).attr("r", 4 / zoomLevel);
                const hoverCircle = d3.select(this.parentNode).select(`circle.hover-circle[cx="${this.getAttribute('cx')}"][cy="${this.getAttribute('cy')}"]`);
                hoverCircle
                    .attr("opacity", 1)
                    .attr("r", 8 / zoomLevel);
                updateTooltip(d);
            })
            .on("mouseout", function() {
                d3.select(this).attr("r", 3 / zoomLevel);
                const hoverCircle = d3.select(this.parentNode).select(`circle.hover-circle[cx="${this.getAttribute('cx')}"][cy="${this.getAttribute('cy')}"]`);
                hoverCircle
                    .attr("opacity", 0)
                    .attr("r", 6 / zoomLevel);
                hideTooltip();
            });
        }

        // Add fixed tooltip
        const tooltip = chartGroup.append("g")
            .attr("class", "tooltip")
            .attr("transform", `translate(${chartSize - 120}, ${chartSize - 50})`)
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
            .attr("fill", "var(--text-color)")
            .attr("opacity", 0.6)
            .attr("font-size", "14px");

        function updateTooltip(d) {
            tooltip.attr("opacity", 1);
            tooltipX.text(`X: ${d.x.toFixed(2)}`);
            tooltipY.text(`Y: ${d.y.toFixed(2)}`);
        }

        function hideTooltip() {
            tooltip.attr("opacity", 0);
        }

        // Add legend
        const legend = chartGroup.append("g")
            .attr("class", "legend")
            .attr("transform", `translate(${chartSize - 100}, 20)`);

        ["Yin", "Yang", "Boundary"].forEach((label, i) => {
            const legendItem = legend.append("g")
                .attr("transform", `translate(0, ${i * 20})`);

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
        });

        // Create sliders
        const sliderWidth = chartSize * 0.8;
        const sliderGroup = d3.select(`#${containerId}`)
            .append("div")
            .attr("class", "sliders")
            .style("width", `${containerSize}px`)
            .style("margin-top", "20px");

        function createSlider(name, min, max, step, value, onChange) {
            if (!visibleControls.includes(name)) return;

            const sliderContainer = sliderGroup.append("div")
                .attr("class", "slider-container")
                .style("margin-bottom", "10px");

            sliderContainer.append("label")
                .attr("for", `${containerId}-${name}-slider`)
                .text(`${name}: `);

            const valueDisplay = sliderContainer.append("span")
                .attr("id", `${containerId}-${name}-value`)
                .text(value);

            sliderContainer.append("input")
                .attr("id", `${containerId}-${name}-slider`)
                .attr("type", "range")
                .attr("min", min)
                .attr("max", max)
                .attr("step", step)
                .attr("value", value)
                .style("width", `${sliderWidth}px`)
                .on("input", function() {
                    const newValue = parseFloat(this.value);
                    valueDisplay.text(newValue.toFixed(2));
                    onChange(newValue);
                });
        }

        createSlider("n", 100, 5000, 100, params.n, (value) => {
            params.n = value;
            updateData();
        });
        createSlider("r_small", 0.01, 0.5, 0.01, params.r_small, (value) => {
            params.r_small = value;
            updateData();
        });
        createSlider("r_big", 0.1, 1.0, 0.01, params.r_big, (value) => {
            params.r_big = value;
            updateData();
        });
        createSlider("zoom", 0.5, 2, 0.1, zoomLevel, (value) => {
            zoomLevel = value;
            const newTransform = d3.zoomIdentity
                .translate(chartSize / 2, chartSize / 2)
                .scale(value)
                .translate(-chartSize / 2, -chartSize / 2);
            chartGroup.call(zoom.transform, newTransform);
        });

        // Zoom slider
        const zoomSliderContainer = sliderGroup.append("div")
            .attr("class", "slider-container")
            .style("margin-bottom", "10px");

        zoomSliderContainer.append("label")
            .attr("for", `${containerId}-zoom-slider`)
            .text("Zoom: ");

        const zoomValueDisplay = zoomSliderContainer.append("span")
            .attr("id", `${containerId}-zoom-value`)
            .text(zoomLevel.toFixed(1));

        const zoomScale = d3.scaleLinear()
            .domain([0.5, 2])
            .range([0, sliderWidth])
            .clamp(true);

        const zoomSlider = zoomSliderContainer.append("input")
            .attr("id", `${containerId}-zoom-slider`)
            .attr("type", "range")
            .attr("min", 0.5)
            .attr("max", 2)
            .attr("step", 0.1)
            .attr("value", zoomLevel)
            .style("width", `${sliderWidth}px`)
            .on("input", function() {
                const newZoom = parseFloat(this.value);
                zoomLevel = newZoom;
                const newTransform = d3.zoomIdentity
                    .translate(chartSize / 2, chartSize / 2)
                    .scale(newZoom)
                    .translate(-chartSize / 2, -chartSize / 2);
                chartGroup.call(zoom.transform, newTransform);
                updateZoomSlider(newZoom);
            });

        function updateZoomSlider(value) {
            zoomValueDisplay.text(value.toFixed(1));
            zoomSlider.property("value", value);
        }

        function updateData() {
            data = generateYinYangData(params.n, params.r_small, params.r_big);
            updateChart();
        }

        // Yin-Yang data generation function
        function generateYinYangData(n, r_small, r_big) {
            const random = new RNG(42);  // Use a fixed seed for consistency
            const pts = [];

            function distToRightDot(x, y) {
                return Math.sqrt((x - 1.5 * r_big)**2 + (y - r_big)**2);
            }

            function distToLeftDot(x, y) {
                return Math.sqrt((x - 0.5 * r_big)**2 + (y - r_big)**2);
            }

            function whichClass(x, y) {
                const d_right = distToRightDot(x, y);
                const d_left = distToLeftDot(x, y);
                const criterion1 = d_right <= r_small;
                const criterion2 = d_left > r_small && d_left <= 0.5 * r_big;
                const criterion3 = y > r_big && d_right > 0.5 * r_big;
                const is_yin = criterion1 || criterion2 || criterion3;
                const is_circles = d_right < r_small || d_left < r_small;

                if (is_circles) return 2;
                return is_yin ? 0 : 1;
            }

            function getSample(goalClass = null) {
                while (true) {
                    const x = random.uniform(0, 2 * r_big);
                    const y = random.uniform(0, 2 * r_big);
                    if (Math.sqrt((x - r_big)**2 + (y - r_big)**2) > r_big) continue;
                    const c = whichClass(x, y);
                    if (goalClass === null || c === goalClass) {
                        const scaled_x = (x / r_big - 1) * 2;
                        const scaled_y = (y / r_big - 1) * 2;
                        return {x: scaled_x, y: scaled_y, class: c};
                    }
                }
            }

            for (let i = 0; i < n; i++) {
                const goalClass = i % 3;
                pts.push(getSample(goalClass));
            }

            return pts;
        }

        // RNG class implementation
        class RNG {
            constructor(seed) {
                this.state = seed;
            }

            random_u32() {
                this.state ^= (this.state >> 12) & 0xFFFFFFFF;
                this.state ^= (this.state << 25) & 0xFFFFFFFF;
                this.state ^= (this.state >> 27) & 0xFFFFFFFF;
                return ((this.state * 0x2545F4914F6CDD1D) >> 32) & 0xFFFFFFFF;
            }

            random() {
                return (this.random_u32() >> 8) / 16777216.0;
            }

            uniform(a = 0.0, b = 1.0) {
                return a + (b - a) * this.random();
            }
        }

        // Initial chart creation
        updateData();
        updateChart();

        // Apply initial zoom
        const initialTransform = d3.zoomIdentity
            .translate(chartSize / 2, chartSize / 2)
            .scale(zoomLevel)
            .translate(-chartSize / 2, -chartSize / 2);
        chartGroup.call(zoom.transform, initialTransform);

        // Expose methods to update the chart if needed
        return {
            updateParams: function(newParams) {
                params = {...params, ...newParams};
                updateData();
            },
            setVisibleControls: function(newVisibleControls) {
                visibleControls = newVisibleControls.includes('zoom') ? newVisibleControls : [...newVisibleControls, 'zoom'];
                // Re-create sliders based on new visible controls
                sliderGroup.selectAll("*").remove();
                createSlider("n", 100, 5000, 100, params.n, (value) => {
                    params.n = value;
                    updateData();
                });
                createSlider("r_small", 0.01, 0.5, 0.01, params.r_small, (value) => {
                    params.r_small = value;
                    updateData();
                });
                createSlider("r_big", 0.1, 1.0, 0.01, params.r_big, (value) => {
                    params.r_big = value;
                    updateData();
                });
                createSlider("zoom", 0.5, 2, 0.1, zoomLevel, (value) => {
                    zoomLevel = value;
                    const newTransform = d3.zoomIdentity
                        .translate(chartSize / 2, chartSize / 2)
                        .scale(value)
                        .translate(-chartSize / 2, -chartSize / 2);
                    chartGroup.call(zoom.transform, newTransform);
                });
            }
        };
    }

    // Expose the function globally
    global.createYinYangChart = createYinYangChart;
})(typeof window !== 'undefined' ? window : this);