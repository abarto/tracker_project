function onGeoSuccess(location) {
    console.log('location', location)

    $("#id_location_description").val(
        "Latitude: " + location.coords.latitude +
        ", Longitude: " + location.coords.longitude + "\n" +
        "City: " + location.address.city + "\n" +
        "Country: " + location.address.country
    );
    $("#id_location_lat").val(location.coords.latitude);
    $("#id_location_lon").val(location.coords.longitude);
    $("#id_name").val("Incident in " + location.address.city + ", " + location.address.country.toUpperCase());
    $("#id_description").val(
        "An incident has occurred in " +
        location.address.city +
        ", " +
        location.address.country.toUpperCase() +
        "."
    );
}

function onGeoError(error) {
    console.log('error', error)
}

$(window).load(function() {
    var options = {
        enableHighAccuracy: true,
        timeout: 6000,
        maximumAge: 0
    };

    geolocator.locate(onGeoSuccess, onGeoError, 1, options, 'map-canvas');
});