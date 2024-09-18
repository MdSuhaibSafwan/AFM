$('#id_currently_living_in').select2({
    placeholder: 'Choose country',
    searchInputPlaceholder: 'Search'
});
$('#id_country').select2({
    placeholder: 'Choose country',
    searchInputPlaceholder: 'Search'
});
$('#id_spoken_languages').select2();
$('#id_level_of_english').select2();
$('#id_programme_level').select2({
    placeholder: 'What level of study are you considering?',
    searchInputPlaceholder: 'Search'
});
//$('#id_area_of_study').select2({
//    placeholder: 'Select a subject field that you are interested in',
//    searchInputPlaceholder: 'Search'
//});
$('#id_intake_year').select2();
$('#id_what_are_you_studying').select2();
$('#id_last_qualification').select2();

//DOB
$( '#id_date_of_birth').datepicker({
          changeYear: true,
          dateFormat: "dd/mm/yy",
          maxDate: '-15yr'
});

$('#id_spoken_languages').select2();
$('#id_gender').select2();
$('#id_study_destination').select2({
    placeholder: 'Select countries where you wish to study',
    searchInputPlaceholder: 'Search'
});

//document.getElementById('get_file').onclick = function () {
//    document.getElementById('id_profile_pic').click();
//}

// Foundation Provider

function currently_study_check(val) {
    if (val == 0) {
        $('#div_id_last_qualification').show();
        $('#div_id_what_are_you_studying').hide();
        $('#id_what_are_you_studying').val('');
        $('#id_last_qualification').attr('required', 'required');
        $('#id_what_are_you_studying').removeAttr('required');
        $('label[for="id_current_or_last_school_name"]').text('Last school name*');

    }
    else {
        $('#div_id_last_qualification').hide();
        $('#id_last_qualification').val('');
        $('#div_id_what_are_you_studying').show();
        $('#id_last_qualification').removeAttr('required');
        $('#id_what_are_you_studying').attr('required', 'required');
        $('label[for="id_current_or_last_school_name"]').text('Current school name*');
    }

}
var value = $('#id_currently_studying').val();
currently_study_check(value);

$('#id_currently_studying').change(function () {
    var value = $(this).val();
    currently_study_check(value);
});

$(function () {
    $("#id_profile_pic").change(function () {
        if (this.files && this.files[0]) {
            var reader = new FileReader();
            reader.onload = function (e) {
                $("#image").attr("src", e.target.result);
                console.log('model loading');
                $("#modalCrop").modal("show");
                console.log('model yes');
            }
            reader.readAsDataURL(this.files[0]);
        }
    });

    var $image = $("#image");
    var cropBoxData;
    var canvasData;
    $("#modalCrop").on("shown.bs.modal", function () {
        $image.cropper({
            viewMode: 1,
            aspectRatio: 1 / 1,
            minCropBoxWidth: 128,
            minCropBoxHeight: 128,
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

    $(".js-zoom-in").click(function () {
        $image.cropper("zoom", 0.1);
    });

    $(".js-zoom-out").click(function () {
        $image.cropper("zoom", -0.1);
    });

    $(".js-crop-and-upload").click(function () {
        var cropData = $image.cropper("getData");
        $("#id_x").val(cropData["x"]);
        $("#id_y").val(cropData["y"]);
        $("#id_height").val(cropData["height"]);
        $("#id_width").val(cropData["width"]);
        $("#modalCrop").modal("hide");
        // $("#ImageformUpload").submit();
    });

});
// Add '+' sign on input for phone number
//$('#id_phone').keyup(function(e) {
//  if (this.value.length < 1) {
//    this.value = '+';
//  } else if (this.value.indexOf('+') !== 0) {
//    this.value = '+' + this.value;
//  }
//});

// Phone number field with country flags and auto updated user's country
var input = document.querySelector("#id_phone");
if(input){
    window.intlTelInput(input, {
        initialCountry: "auto",
        geoIpLookup: function(success, failure) {
            $.get("https://ipinfo.io", function() {}, "jsonp").always(function(resp) {
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
function select_default_country_select2(field_id, country){
    if ($("#" + field_id).val() == ''){
        $("#" + field_id).val(country);
        $("#" + field_id).select2().trigger('change');
    }
}

// Get country code by IP
$.get("https://ipinfo.io", function (response) {
    if(response){
        if(response.country){
            select_default_country_select2('id_currently_living_in', response.country);
        }
    }
//    console.log(JSON.stringify(response, null, 4));
}, "jsonp");


// Check if applicant is looking for countries in EU
function check_if_applicant_is_looking_for_EU_countries(){
    var country_living_in = $("#id_currently_living_in").val();
    var study_destination = $("#id_study_destination").val();
    // The EU countries are:
    // United Kingdom, Austria, Belgium, Bulgaria, Croatia, Republic of Cyprus, Czech Republic, Denmark, Estonia, Finland, France,
    // Germany, Greece, Hungary, Ireland, Italy, Latvia, Lithuania, Luxembourg, Malta, Netherlands, Poland, Portugal,
    // Romania, Slovakia, Slovenia, Spain and Sweden.

    EU_countries = ['GB', 'AT', 'BE', 'BG', 'HR', 'CY', 'CZ', 'DK', 'EE', 'FI', 'FR', 'DE', 'GR', 'HU', 'IE', 'IT',
                'LV', 'LT', 'LU', 'MT', 'NL', 'PL', 'PT', 'RO', 'SK', 'SI', 'ES', 'SE']
    show = false
    if (EU_countries.indexOf(country_living_in) > -1){
        if(study_destination){
            if (Object.values(study_destination).includes('GB')){
                show = true;
            }
        }
    }
//    if (country_living_in == 'GB' ){
//        if(study_destination){
//            for(country in EU_countries){
//                if (Object.values(study_destination).includes(EU_countries[country])){
//                    show = true;
//                }
//            }
//        }
//    }
    if (show){
        $("#hint_id_study_destination").show();
    }
    else{
        $("#hint_id_study_destination").hide();
    }
}
//$(".application-notice").hide();
check_if_applicant_is_looking_for_EU_countries();
$('#id_currently_living_in').on("change", function (e) {
    check_if_applicant_is_looking_for_EU_countries();
});
$('#id_study_destination').on("change", function (e) {
    check_if_applicant_is_looking_for_EU_countries();
});