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
        zoom: zoomLevel
    };

    var infoWindow = new google.maps.InfoWindow({
        content: ''
    });

    map = new google.maps.Map($("#map-canvas").get(0), mapOptions);
    setMarker(locationLatlng, map);

    google.maps.event.addListener(map, "click", function(event) {
        setMarker(event.latLng, map);
    });
    google.maps.event.addListener(map, "rightclick", function(event) {
        var latLng = event.latLng;

        $infoWindowContent = $("<div><span>Latitude: " + latLng.lat() + "</span><br/><span>Longitude: " + latLng.lng() + "</span><br/>" + "<a class=\"btn btn-default btn-xs btn-block\">Place marker</a></div>");
        $infoWindowContent.find("a").click(function() {
            infoWindow.close();
            setMarker(infoWindow.getPosition(), map);
        });

        infoWindow.setContent($infoWindowContent.get(0));
        infoWindow.setPosition(event.latLng);

        infoWindow.open(map);
    });
}