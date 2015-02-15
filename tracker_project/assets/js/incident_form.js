var map;
var marker;

function setLocation(latLng) {
    $("#id_location_x").val(latLng.lat());
    $("#id_location_y").val(latLng.lng());
}

function initializeMap(locationLatitude, locationLongitude, zoomLevel) {
    var locationLatlng = new google.maps.LatLng(locationLatitude, locationLongitude);

    var mapOptions = {
        center: locationLatlng,
        mapTypeId: google.maps.MapTypeId.HYBRID,
        zoom: zoomLevel
    };

    map = new google.maps.Map($("#map-canvas").get(0), mapOptions);
    marker = new google.maps.Marker({
        position: locationLatlng,
        map: map,
    });

    setLocation(marker.position);

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

        setLocation(marker.position);
    });
}