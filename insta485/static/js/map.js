const map = L
    .map('mapid')
    .setView([47, 2], 2);

// Add map layer
L.tileLayer(
    'https://cartodb-basemaps-b.global.ssl.fastly.net/light_nolabels/{z}/{x}/{y}.png', {
    attribution: 'Map data &copy; <a href="https://carto.com/">Carto</a>',
    maxZoom: 6,
    minZoom: 2,
    }).addTo(map);

L.svg().addTo(map);
    
// Get data
let markers = []
let m = fetch('/api/v1/map/')
    .then(response => {
        if (!response.ok) throw Error(response.statusText);
        return response.json();
    })
    .then(data => {
        // const markers = [
        //     {long: 9.083, lat: 42.149}, // corsica
        //     {long: 7.26, lat: 43.71}, // nice
        //     {long: 2.349, lat: 48.864}, // Paris
        //     {long: -1.397, lat: 43.664}, // Hossegor
        //     {long: 3.075, lat: 50.640}, // Lille
        //     {long: -3.83, lat: 48}, // Morlaix
        // ];
        let markers = []
        for (var key in data.map_counts) {
            markers.push(data.map_counts[key]);
        }
        console.log(markers)

        const Tooltip = d3.select("#mapid")
            .append("div")
            .attr("class", "tooltip")
            .style("opacity", 1)
            .style("background-color", "white")
            .style("border", "solid")
            .style("border-width", "2px")
            .style("border-radius", "5px")
            .style("padding", "5px")
        
        const mouseover = function(event, d) {
            Tooltip.style("opacity", 1)
        }
        var mousemove = function(event, d) {
            Tooltip
                .html("Tooltip")
                .style("left", (event.x)/2 + "px")
                .style("top", (event.y)/2 - 30 + "px")
        }
        var mouseleave = function(event, d) {
            Tooltip.style("opacity", 0)
        }

        d3.select("#mapid")
            .select("svg")
            .selectAll("myCircles")
            .data(markers)
            .join("circle")
                .attr("cx", d => map.latLngToLayerPoint([d.lat, d.lon]).x)
                .attr("cy", d => map.latLngToLayerPoint([d.lat, d.lon]).y)
                .attr("r", d => d.count)
                .style("fill", "red")
                .attr("stroke", "red")
                .attr("stroke-width", 3)
                .attr("fill-opacity", .4)
            .on("mouseover", mouseover)
            .on("mousemove", mousemove)
            .on("mouseleave", mouseleave)
        
        // Function that update circle position if something change
        function update() {
            d3.selectAll("circle")
                .attr("cx", d => map.latLngToLayerPoint([d.lat, d.lon]).x)
                .attr("cy", d => map.latLngToLayerPoint([d.lat, d.lon]).y)
            }

        // If the user change the map (zoom or drag), I update circle position:
        map.on("moveend", update)
    })
    .catch(response =>
        console.log(response)
    )