// Get data
let m = fetch('/api/v1/map/')
    .then(response => {
        if (!response.ok) throw Error(response.statusText);
        return response.json();
    })
    .then(data => {
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

        let markers = []
        for (var key in data.map_counts) {
            markers.push(data.map_counts[key]);
        }
        
        for (var key in markers) {
            var circle = L.circle([markers[key].lat, markers[key].lon], {
                color: 'red',
                fillColor: '#f03',
                fillOpacity: 0.5,
                radius: markers[key].count
            }).addTo(map);
            circle.bindPopup(`${markers[key].name}: ${(markers[key].count - 50000) / 15000}`);
        }
    })
    .catch(response =>
        console.log(response)
    )