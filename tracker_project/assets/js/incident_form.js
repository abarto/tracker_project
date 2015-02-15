var map;
var marker;

$(window).load(function() {
    var mapOptions = {
        center: new google.maps.LatLng(0, 0),
        mapTypeId: google.maps.MapTypeId.HYBRID,
        zoom: 2
    };

    map = new google.maps.Map($("#map-canvas").get(0), mapOptions);

    if ($("#id_location_geojson").val() !== "") {
        locationGeoJson = $.parseJSON($("#id_location_geojson").val());

        marker = new google.maps.Marker({
            position: toLatLng(locationGeoJson),
            map: map
        });

        map.setCenter(marker.position);
        map.setZoom(8);
    }

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
        if (typeof marker !== "undefined" && marker !== null) {
            marker.setMap(null);
        }

        marker = event_marker;
        $("#id_location_geojson").val(JSON.stringify(fromLatLng(marker.position)));
    });
});