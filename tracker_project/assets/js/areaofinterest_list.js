$(function() {
    var areaOfInterestModalImgSrcTemplate = Handlebars.compile($.trim($("#area-of-interest-modal-img-src-template").html()));

    $(".area-of-interest-centroid").click(function(event) {
        var $eventTarget = $(event.target);
        var $areaOfInterestModal = $("#areaOfInterestModal");

        var name = $eventTarget.data("name");
        var path = $eventTarget.data("path");
        var latitude = $eventTarget.data("latitude");
        var longitude = $eventTarget.data("longitude");

        $areaOfInterestModal.find("#areaOfInterestModalTitle").text(name);
        $areaOfInterestModal.find("img").attr(
            "src",
            areaOfInterestModalImgSrcTemplate({
                path: path
            })
        );

        $areaOfInterestModal.modal('show');
    });
});