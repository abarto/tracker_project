function fromLatLng(latLng) {
    return {
        "type": "Point",
        "coordinates": [
            latLng.lng(),
            latLng.lat()
        ]
    }
}

function toLatLng(geoJson) {
    return new google.maps.LatLng(
        geoJson.coordinates[1],
        geoJson.coordinates[0]
    );
}

function fromPolygon(polygon) {
    var coordinates = [[]];

    polygon.getPath().forEach(function (latLng) {
        coordinates[0].push([latLng.lng(), latLng.lat()]);
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
            new google.maps.LatLng(coordinates[coordinate][1], coordinates[coordinate][0])
        );
    }

    var polygon = new google.maps.Polygon({
        paths: paths,
    });

    return polygon;
}