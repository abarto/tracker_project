$(function() {
    $(".incident-location").click(function(event) {
        var $eventTarget = $(event.target);
        var $incidentLocationModal = $("#incidentLocationModal");

        var name = $eventTarget.data("name");
        var longitude = $eventTarget.data("longitude");
        var latitude = $eventTarget.data("latitude");

        $incidentLocationModal.find("#incidentLocationModalTitle").text(name);
        $incidentLocationModal.find("img").attr(
            "src",
            "https://maps.googleapis.com/maps/api/staticmap?size=512x512&zoom=15&maptype=hybrid&center=" + latitude + "," + longitude +"&markers=color:red|label:Location|" + latitude + "," + longitude
        );

        $incidentLocationModal.modal('show');
    });
});