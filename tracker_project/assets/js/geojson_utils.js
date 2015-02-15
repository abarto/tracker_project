function fromLatLng(latLng) {
    return {
        "type": "Point",
        "coordinates": [
            latLng.lat(),
            latLng.lng(),
        ]
    }
}

function toLatLng(geoJson) {
    return new google.maps.LatLng(
        geoJson.coordinates[0],
        geoJson.coordinates[1]
    );
}

function fromPolygon(polygon) {
    var coordinates = [[]];

    polygon.getPath().forEach(function (latLng) {
        coordinates[0].push([latLng.lat(), latLng.lng()]);
    });
    coordinates[0].push(coordinates[0][0]);

    var geoJson = {
        "type": "Polygon",
        "coordinates": coordinates
    };

    return geoJson;
}

function toPolygon(geoJson) {
    var coordinates = geoJson.coordinates[0];
    var paths = [];

    for (coordinate in coordinates) {
        paths.push(
            new google.maps.LatLng(coordinates[coordinate][0], coordinates[coordinate][1])
        );
    }

    var polygon = new google.maps.Polygon({
        paths: paths,
    });

    return polygon;
}