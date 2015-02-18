var map;
var infoWindow;

function buildAlertModalBodyHtml(notification) {
    var $alertModalBodyHtml = $("<div></div>");

    var feature = notification.feature

    var $title = $("<div class=\"alert alert-warning\" role=\"alert\"></div>");
    $title.html(
        'Incident (' +
        notification.feature.properties.severity +
        '): <a href=\"' +
        notification.url +
        "\">" +
        notification.feature.properties.name +
        "</a>"
    )

    $alertModalBodyHtml.append($title);
    $alertModalBodyHtml.append($("<h4>Areas of Interest:</h4>"))

    var areas_of_interest = notification.areas_of_interest

    var $list_group = $("<ul class=\"list-group\"></ul>");
    for (area_of_interest in areas_of_interest) {
        $list_group.append(
            $(
                "<li class=\"list-group-item\">" +
                areas_of_interest[area_of_interest].name +
                "<span class=\"label label-default pull-right\">" +
                areas_of_interest[area_of_interest].severity +
                "</span>" +
                "</li>"
            )
        );
    }

    $alertModalBodyHtml.append($list_group);

    return $alertModalBodyHtml;
}

function showAlert(alertModalBodyHtml) {
    var $alertModal = $("#alertModal");

    $alertModal.find("#alertModalBody").html(alertModalBodyHtml);

    $alertModal.modal('show');
}

$(window).load(function() {
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
        event.feature.toGeoJson(function(object) {
            infoWindow.setContent("<div><pre>" + JSON.stringify(object, null, '  ') + "</pre></div>");

            var anchor = new google.maps.MVCObject();
            anchor.set("position", event.latLng);

            infoWindow.open(map, anchor);
        });
    });
});

$(function() {
    var socket = io.connect("/notifications");

    socket.on('connect', function(){
        console.log('connect', socket);
    });
    socket.on('notification', function(notification){
        if (notification.type === "post_save") {
            if (notification.created) {
                map.data.addGeoJson(notification.feature);
            } else {
                var feature = map.data.getFeatureById(notification.feature.id);
                map.data.remove(feature);

                map.data.addGeoJson(notification.feature);
            }
        } else if (notification.type === "post_delete") {
            var feature = map.data.getFeatureById(notification.feature.id);
            map.data.remove(feature);
        } else if (notification.type === "alert") {
            showAlert(buildAlertModalBodyHtml(notification))
        } else {
            console.log(notification);
        }
    });
    socket.on('disconnect', function(){
        console.log('disconnect', socket);
    });
});