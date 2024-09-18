$(document).ready(function() {
console.log("-------------------------Student profile Javascript loaded-----------------------");
$('#id_date_of_birth').datepicker({
    changeYear: true,
    dateFormat: "dd/mm/yy",
    maxDate: '-18yr'
});

$('#id_dbs_date').datepicker({
    changeYear: true,
    dateFormat: "dd/mm/yy",
});

$('#id_spoken_languages').select2({
    placeholder: ' Select Language',
    searchInputPlaceholder: 'Search'
});

$('#id_hobbies').select2({
    placeholder: 'Select Hobby',
    searchInputPlaceholder: 'Search'
});

$('#id_studying_in').select2();

$('#id_subject_foundation').select2();
$('#id_currently_living_in').select2({
    placeholder: 'Choose country',
    searchInputPlaceholder: 'Search'
});

$('#id_country').select2({
    placeholder: 'Select country',
    searchInputPlaceholder: 'Search'
});

$('#id_where_did_you_study').select2({
    placeholder: 'Choose Here',
});

$('#id_studying_in').select2({
    placeholder: 'Choose country',
    searchInputPlaceholder: 'Search'
});

$('#id_preferred_career_field').select2({
    placeholder: 'Select',
    searchInputPlaceholder: 'Search'
});

$('#id_preferred_location').select2({
    placeholder: 'Select',
    searchInputPlaceholder: 'Search'
});

$('#id_where_will_you_be_during_the_completion_of_your_internship').select2({
    placeholder: 'Select',
    searchInputPlaceholder: 'Search'
});

$('#id_institute_list').select2({
    placeholder: 'Select',
    searchInputPlaceholder: 'Search'
});

$('#id_duration_of_internship').select2();
$('#id_weekly_working_hours').select2();

$('#id_phone_0').select2({
    placeholder: 'Choose Country',
    searchInputPlaceholder: 'Search'
});

function set_custom_validity(field, validity) {
    if (field) {
        field.setCustomValidity(validity);
    }
}


// About me

$(document).ready(function () {
    console.log("About me triggered.....");
    $('#div_id_about_me label').append('<span id="word_count"></span>');
    $("#id_about_me").on('keyup', function () {
        var words = 0;

        if ((this.value.match(/\S+/g)) != null) {
            //      words = this.value.replace(/ /g,'').length;
            words = this.value.length;
        }

        if (words > 500) {
            this.value = this.value.substring(0, 500);
        }
        else {
            var word_count = 500 - words
            $('#word_count').text("( Characters Left : " + word_count + " )");
        }
    });  
});




// Save Button
if ($('#id_consent1').is(':checked') && $('#id_media_consent').is(':checked')) {
    $('#Button').removeClass('not-active');
}
else {
    $('#Button').addClass('not-active');
}
$("input[type=checkbox]").change(function () {
    if ($('#id_consent1').is(':checked') && $('#id_media_consent').is(':checked')) {
        $('#Button').removeClass('not-active');
    }
    else {
        $('#Button').addClass('not-active');
    }
});



// Profile pic upload
function placeVal(x, y, width, height, rotation) {
    $("#id_x").val(cropData["x"]);
    $("#id_y").val(cropData["y"]);
    $("#id_height").val(cropData["height"]);
    $("#id_width").val(cropData["width"]);
    $("#id_rotation").val(rotation_degree);
}
$('.dropzone').click(function () { $("input[name='profile_pic']").trigger('click'); });
let rotation_degree = 0;
var cropData;
let preview_clone;
$(function () {
    $("input[name='profile_pic']").change(function () {
        if (this.files && this.files[0] && this.files[0].name.match(/\.(jpg|jpeg|png|gif)$/)) {
            var reader = new FileReader();
            reader.onload = function (e) {
                $("#profile_pic").attr("src", e.target.result);
                $("#feature_image_modal_crop").modal("show");
            }
            reader.readAsDataURL(this.files[0]);
        }
        else {
            alert("Please upload image in one of these formats ' jpg | jpeg | png | gif '.");
            $("input[name='profile_pic']").val('');
        }
    });
    var $image = $("#profile_pic");
    var cropBoxData;
    var canvasData;
    $("#feature_image_modal_crop").on("shown.bs.modal", function () {
        $image.cropper({
            viewMode: 1,
            aspectRatio: 300 / 300,
            minCropBoxWidth: 300,
            minCropBoxHeight: 300,
            preview: '.preview_profile_pic',
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
        $('.js-zoom-in-one').trigger('click');
        $('.js-zoom-out-one').trigger('click');
        $('.js-zoom-in-one').trigger('click');
        $('.js-zoom-out-one').trigger('click');
        $image.cropper("rotate", -90);
        rotation_degree = rotation_degree + 90;
        if (rotation_degree == 360) {
            rotation_degree = 0;
        }
        cropData = $image.cropper("getData");
        placeVal(cropData["x"], cropData["y"], cropData["height"], cropData["width"], rotation_degree);
    });
    $(".js-crop-and-upload-one").click(function () {
        preview_clone = $('.preview_profile_pic').clone();
        cropData = $image.cropper("getData");
        placeVal(cropData["x"], cropData["y"], cropData["height"], cropData["width"], rotation_degree);
        $("#feature_image_modal_crop").modal("hide");
    });

    $('#feature_image_modal_crop').on('hidden.bs.modal', function () {
        $('#preview-clone-profile_pic').html(preview_clone);
    })

    $('.cancel_btn').click(function () {
        $("input[name='profile_pic']").val('');
    })
});


// Phone number field with country flags and auto updated user's country
var input = document.querySelector("#id_phone");
if (input) {
    window.intlTelInput(input, {
        initialCountry: "auto",
        geoIpLookup: function (success, failure) {
            $.get("https://ipinfo.io", function () { }, "jsonp").always(function (resp) {
                var countryCode = (resp && resp.country) ? resp.country : "us";
                success(countryCode);
            });
        },
        hiddenInput: "phone",
        separateDialCode: true,
        utilsScript: '/static/js/utils.js',
    });
}

// Check default country of select2 drop-down
function select_default_country_select2(field_id, country) {
    if ($("#" + field_id).val() == '') {
        $("#" + field_id).val(country);
        $("#" + field_id).select2().trigger('change');
    }
}

// Get country code by IP
$.get("https://ipinfo.io", function (response) {
    if (response) {
        if (response.country) {
            select_default_country_select2('id_currently_living_in', response.country);
        }
    }
    //    console.log(JSON.stringify(response, null, 4));
}, "jsonp");


});