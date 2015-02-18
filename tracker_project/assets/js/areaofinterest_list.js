$(function() {
    $(".area-of-interest-centroid").click(function(event) {
        var $eventTarget = $(event.target);
        var $areaOfInterestModal = $("#areaOfInterestModal");

        var name = $eventTarget.data("name");
        var path = $eventTarget.data("path");

        $areaOfInterestModal.find("#areaOfInterestModalTitle").text(name);
        $areaOfInterestModal.find("img").attr(
            "src",
            "https://maps.googleapis.com/maps/api/staticmap?size=512x512&maptype=hybrid&center={{ object.polygon.centroid.x }},{{ object.polygon.centroid.y }}&path=color:0xff0000ff|fillcolor:0xff000044|weight:5|" + path
        );

        $areaOfInterestModal.modal('show');
    });
});