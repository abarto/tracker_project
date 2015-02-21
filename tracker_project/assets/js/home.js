var map;
var infoWindow;

function buildAlertModalBodyHtml(notification) {
    var $alertModalBodyHtml = $("<div></div>");

    var feature = notification.feature

    var $title = $("<div class=\"alert alert-warning\" role=\"alert\"></div>");
    $title.html(
        "<span class=\"glyphicon glyphicon-map-marker\" aria-hidden=\"true\"></span>&nbsp;Incident: <a class=\"alert-link\" href=\"" +
        notification.feature.properties.url +
        "\">" +
        notification.feature.properties.name +
        "</a>" +
        "<span class=\"label label-default pull-right\">" +
        notification.feature.properties.severity +
        "</span>"
    )

    $alertModalBodyHtml.append($title);
    $alertModalBodyHtml.append($("<h4>Areas of Interest:</h4>"))

    var areas_of_interest = notification.areas_of_interest

    var $list_group = $("<ul class=\"list-group\"></ul>");
    for (area_of_interest in areas_of_interest) {
        $list_group.append(
            $(
                "<li class=\"list-group-item\">" +
                "<span class=\"glyphicon glyphicon-search\" aria-hidden=\"true\"></span>&nbsp;<a href=\"" +
                areas_of_interest[area_of_interest].url +
                "\">" +
                areas_of_interest[area_of_interest].name +
                "</a><span class=\"label label-default pull-right\">" +
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

function buildInfoWindowContent(feature) {
    var content =
        "<div class=\"panel panel-default info-window-panel\">" +
        "<div class=\"panel-heading\"><a href=\"" + feature.getProperty("url") + "\">" + feature.getId() + "</a></div>" +
        "<div class=\"panel-body\">" +
        "<dl>" +
        "<dt>Model</dt>" +
        "<dd>" + feature.getProperty("model") + "</dd>" +
        "<dt>Name</dt>" +
        "<dd>" + feature.getProperty("name") + "</dd>" +
        "<dt>Severity</dt>" +
        "<dd><span class=\"label label-default\">" + feature.getProperty("severity") + "</span></dd>" +
        "</dl>" +
        "</div>" +
        "</div>"

    return content;
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
        infoWindow.setContent(buildInfoWindowContent(event.feature));

        var anchor = new google.maps.MVCObject();
        anchor.set("position", event.latLng);

        infoWindow.open(map, anchor);
    });
});

$(function() {
    var socket = io.connect(
        "/notifications",
        {
            "reconnectionDelay": 5000,
            "timeout": 10000
        }
    );

    socket.on('connect', function(){
        console.log('connect', socket);
    });
    socket.on('notification', function(notification){
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
            showAlert(buildAlertModalBodyHtml(notification))
        } else {
            console.log(notification);
        }
    });
    socket.on('disconnect', function(){
        console.log('disconnect', socket);
    });
});