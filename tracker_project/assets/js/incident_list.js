$(function() {
    var incidentLocationModalImgSrcTemplate = Handlebars.compile($.trim($("#incident-location-modal-img-src-template").html()));

    $(".incident-location").click(function(event) {
        var $eventTarget = $(event.target);
        var $incidentLocationModal = $("#incidentLocationModal");

        var name = $eventTarget.data("name");
        var longitude = $eventTarget.data("longitude");
        var latitude = $eventTarget.data("latitude");

        $incidentLocationModal.find("#incidentLocationModalTitle").text(name);
        $incidentLocationModal.find("img").attr(
            "src",
            incidentLocationModalImgSrcTemplate({
                latitude: latitude,
                longitude: longitude
            })
        );

        $incidentLocationModal.modal('show');
    });
});