var map = null;
var marker = null;
var infoWindow = null;

function setMarker(latLng, map) {
    if (marker !== null) {
        marker.setMap(null);
    }

    marker = new google.maps.Marker({
        position: latLng,
        map: map,
    });

    $("#id_location_x").val(latLng.lat());
    $("#id_location_y").val(latLng.lng());
}

function initializeMap(locationLatitude, locationLongitude, zoomLevel) {
    var locationLatlng = new google.maps.LatLng(locationLatitude, locationLongitude);

    var mapOptions = {
        center: locationLatlng,
        mapTypeId: google.maps.MapTypeId.HYBRID,
        zoom: zoomLevel,
        draggableCursor: 'crosshair'
    };

    var $placeMarkerButton = $("<a class=\"btn btn-default btn-xs\"><span class=\"glyphicon glyphicon-map-marker\" aria-hidden=\"true\"></span>&nbsp;Place marker here</a>");
    $placeMarkerButton.click(function() {
        infoWindow.close();
        setMarker(infoWindow.getPosition(), map);
    });

    infoWindow = new google.maps.InfoWindow({
        content: $placeMarkerButton.get(0)
    });

    map = new google.maps.Map($("#map-canvas").get(0), mapOptions);
    setMarker(locationLatlng, map);

    google.maps.event.addListener(map, "click", function(event) {
        setMarker(event.latLng, map);
    });
    google.maps.event.addListener(map, "rightclick", function(event) {
        var latLng = event.latLng;

        infoWindow.setPosition(event.latLng);

        infoWindow.open(map);
    });
}