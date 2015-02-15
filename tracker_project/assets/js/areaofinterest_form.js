var map;
var polygon;

$(window).load(function() {
    var mapOptions = {
        mapTypeId: google.maps.MapTypeId.HYBRID,
        center: new google.maps.LatLng(0, 0),
        zoom: 4
    };

    map = new google.maps.Map($("#map-canvas").get(0), mapOptions);

    if ($("#id_polygon_geojson").val() !== "") {
        polygonGeoJson = $.parseJSON($("#id_polygon_geojson").val());

        polygon = toPolygon(polygonGeoJson);
        polygon.setMap(map);

        var bounds = new google.maps.LatLngBounds();
        polygon.getPath().forEach(function(latLng) {
            bounds.extend(latLng);
        });

        map.fitBounds(bounds);
    }

    var drawingManager = new google.maps.drawing.DrawingManager({
        drawingMode: google.maps.drawing.OverlayType.POLYGON,
        drawingControl: true,
        drawingControlOptions: {
            position: google.maps.ControlPosition.TOP_CENTER,
            drawingModes: [
                google.maps.drawing.OverlayType.POLYGON,
            ]
        }
    });
    drawingManager.setMap(map);

    google.maps.event.addListener(drawingManager, 'polygoncomplete', function(event_polygon) {
        if (typeof polygon !== "undefined" && polygon !== null) {
            polygon.setMap(null);
        }

        polygon = event_polygon;
        $("#id_polygon_geojson").val(JSON.stringify(fromPolygon(polygon)));
    });
});