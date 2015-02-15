$(window).load(function() {
    var mapOptions = {
        center: new google.maps.LatLng(0, 0),
        mapTypeId: google.maps.MapTypeId.HYBRID,
        zoom: 2
    };

    map = new google.maps.Map($("#map-canvas").get(0), mapOptions);
});