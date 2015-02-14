$(function() {
    $(".incident-location").click(function(event) {
        var $eventTarget = $(event.target);
        var $incidentLocationModel = $("#incidentLocationModal");

        var name = $eventTarget.data("name");
        var longitude = $eventTarget.data("longitude");
        var latitude = $eventTarget.data("latitude");

        $incidentLocationModel.find("#incidentLocationModalLabel").text(name);
        $incidentLocationModel.find("img").attr(
            "src",
            "https://maps.googleapis.com/maps/api/staticmap?size=512x512&zoom=15&maptype=hybrid&center=" + longitude + "," + latitude +"&markers=color:red|label:Location|" + longitude + "," + latitude
        );

        $incidentLocationModel.modal('show');
    });
});