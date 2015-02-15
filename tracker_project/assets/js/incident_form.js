var map;
var marker;

function fromLatLng(latLng) {
    return {
        "type": "Point",
        "coordinates": [
            latLng.lat(),
            latLng.lng(),
        ]
    }
}

function toLatLng(geoJsonFeature) {
    return new google.maps.LatLng(
        locationGeoJson.coordinates[0],
        locationGeoJson.coordinates[1]
    );
}

function initializeMap() {
    locationGeoJson = $.parseJSON($("#id_location_geojson").val());

    var locationLatLng = toLatLng(locationGeoJson);

    var mapOptions = {
        center: locationLatLng,
        mapTypeId: google.maps.MapTypeId.HYBRID,
        zoom: 8
    };

    map = new google.maps.Map($("#map-canvas").get(0), mapOptions);
    marker = new google.maps.Marker({
        position: locationLatLng,
        map: map
    });

    var drawingManager = new google.maps.drawing.DrawingManager({
        drawingMode: google.maps.drawing.OverlayType.MARKER,
        drawingControl: true,
        drawingControlOptions: {
            position: google.maps.ControlPosition.TOP_CENTER,
            drawingModes: [
                google.maps.drawing.OverlayType.MARKER,
            ]
        }
    });
    drawingManager.setMap(map);

    google.maps.event.addListener(drawingManager, 'markercomplete', function(event_marker) {
        marker.setMap(null);

        marker = event_marker;
        $("#id_location_geojson").val(JSON.stringify(fromLatLng(marker.position)));
    });
}