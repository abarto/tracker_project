var map;
var infoWindow;
var infoWindowContentsTemplate;
var alertModalBodyTemplate;

function showAlert(notification) {
    var $alertModal = $("#alertModal");

    $alertModal.find("#alertModalBody").html(
        alertModalBodyTemplate({
            notification: notification
        })
    );
    $alertModal.modal('show');
}

$(window).load(function() {
    infoWindowContentsTemplate = Handlebars.compile($("#info-window-contents-template").html());
    alertModalBodyTemplate = Handlebars.compile($("#alert-modal-body-template").html());

    var mapOptions = {
        center: new google.maps.LatLng(0, 0),
        mapTypeId: google.maps.MapTypeId.HYBRID,
        zoom: 2
    };

    map = new google.maps.Map($("#map-canvas").get(0), mapOptions);

    map.data.loadGeoJson(incidentFeatureCollectionUrl);
    map.data.loadGeoJson(areaOfInterestFeatureCollectionUrl);

    infoWindow = new google.maps.InfoWindow({
        content: ""
	  });

    map.data.addListener('click', function(event) {
        console.log(event.feature);

        infoWindow.setContent(
            infoWindowContentsTemplate({
                id: event.feature.getProperty("id"),
                url: event.feature.getProperty("url"),
                model: event.feature.getProperty("model"),
                name: event.feature.getProperty("name"),
                severity: event.feature.getProperty("severity")
            })
        );

        var anchor = new google.maps.MVCObject();
        anchor.set("position", event.latLng);

        infoWindow.open(map, anchor);
    });
});

$(function() {
    var socket = new WebSocket(webSocketUrl);

    socket.onopen = function(event) {
        console.log('open', event);
    }
    socket.onmessage = function(event) {
        console.log('message', event);

        var notification = $.parseJSON(event.data);

        console.log('notification', notification);

        if (notification.type === "post_save") {
            if (notification.created) {
                map.data.addGeoJson(notification.feature);
            } else {
                var feature = map.data.getFeatureById(notification.feature.id);
                map.data.remove(feature);

                if (! notification.feature.properties.closed) {
                    map.data.addGeoJson(notification.feature);
                }
            }
        } else if (notification.type === "post_delete") {
            var feature = map.data.getFeatureById(notification.feature.id);
            map.data.remove(feature);
        } else if (notification.type === "alert") {
            showAlert(notification);
        } else {
            console.log(notification);
        }
    }
    socket.onclose = function(event) {
        console.log('close', event);
    }
    socket.onerror = function(event) {
        console.log('error', event);
    }
});
