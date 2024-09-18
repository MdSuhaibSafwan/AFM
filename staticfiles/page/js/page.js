// Profile pic upload
function placeVal(x,y, width, height, rotation){
    $("#id_x").val(cropData["x"]);
    $("#id_y").val(cropData["y"]);
    $("#id_height").val(cropData["height"]);
    $("#id_width").val(cropData["width"]);
    $("#id_rotation").val(rotation_degree);
}
//$('.dropzone').click(function(){ $("input[name='feature_image']").trigger('click'); });
let rotation_degree = 0;
var cropData;
let preview_clone;

$(function () {
    $("input[name='feature_image']").change(function () {
        if (this.files && this.files[0]) {
            var reader = new FileReader();
            reader.onload = function (e) {
                $("#feature_image").attr("src", e.target.result);
                $("#feature_image_modal_crop").modal("show");
            }
            reader.readAsDataURL(this.files[0]);
        }
    });
    var $image = $("#feature_image");
    var cropBoxData;
    var canvasData;
    $("#feature_image_modal_crop").on("shown.bs.modal", function () {
        $image.cropper({
            viewMode: 1,
            aspectRatio: 500 / 500,
            minCropBoxWidth: 500,
            minCropBoxHeight: 500,
            preview: '.preview_feature_image',
            ready: function () {
                $image.cropper("setCanvasData", canvasData);
                $image.cropper("setCropBoxData", cropBoxData);
            }
        });
    }).on("hidden.bs.modal", function () {
        cropBoxData = $image.cropper("getCropBoxData");
        canvasData = $image.cropper("getCanvasData");
        $image.cropper("destroy");
    });
    $(".js-zoom-in-one").click(function () {
        $image.cropper("zoom", 0.1);
        cropData = $image.cropper("getData");
        placeVal(cropData["x"], cropData["y"], cropData["height"], cropData["width"], rotation_degree);
    });
    $(".js-zoom-out-one").click(function () {
        $image.cropper("zoom", -0.1);
        cropData = $image.cropper("getData");
        placeVal(cropData["x"], cropData["y"], cropData["height"], cropData["width"], rotation_degree);
    });
    $(".rotateL").click(function () {
        $image.cropper("rotate", -90);
        rotation_degree = rotation_degree + 90;
        if(rotation_degree==360){
            rotation_degree = 0;
        }
        cropData = $image.cropper("getData");
        placeVal(cropData["x"], cropData["y"], cropData["height"], cropData["width"], rotation_degree);
    });
    $(".js-crop-and-upload-one").click(function () {
        preview_clone = $('.preview_feature_image').clone();
        cropData = $image.cropper("getData");
        placeVal(cropData["x"], cropData["y"], cropData["height"], cropData["width"], rotation_degree);
        $("#feature_image_modal_crop").modal("hide");
    });

    $('#feature_image_modal_crop').on('hidden.bs.modal', function () {
        $('#preview-clone-feature_image').html(preview_clone);
    })

    $('.cancel_btn').click(function(){
        $("input[name='feature_image']").val('');
    })
});

// About me

//  $(document).ready(function() {
//      $("#id_content").bind('input propertychange', function() {
//        var words = 0;
//
//        if ((this.value.match(/\S+/g)) != null) {
//    //      words = this.value.replace(/ /g,'').length;
//          words = this.value.length;
//        }
//        alert('words: '+ words);
//
//    });
//  });
