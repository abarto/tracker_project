var map = null;
var marker = null;

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
        zoom: zoomLevel
    };

    map = new google.maps.Map($("#map-canvas").get(0), mapOptions);
    setMarker(locationLatlng, map);

    google.maps.event.addListener(map, 'click', function(event) {
        setMarker(event.latLng, map);
    });
}