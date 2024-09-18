$( '#id_date_of_birth').datepicker({
  changeYear: true,
  dateFormat: "dd/mm/yy",
  maxDate: '-18yr'
});
$( '#id_dbs_date').datepicker({
  changeYear: true,
  dateFormat: "dd/mm/yy",
});

$('#id_spoken_languages').select2({
    placeholder: 'Choose Language',
    searchInputPlaceholder: 'Search'
});

$('#id_hobbies').select2({
    placeholder: 'Select',
    searchInputPlaceholder: 'Search'
});


$('#id_studying_in').select2();

$('#id_subject_foundation').select2();
$('#id_currently_living_in').select2({
    placeholder: 'Choose country',
    searchInputPlaceholder: 'Search'
});

$('#id_country').select2({
    placeholder: 'Choose country',
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
function set_custom_validity(field, validity){
    if(field){
        field.setCustomValidity(validity);
    }
}
$('.div_year').hide();
$('.div_study_year').show();
if($('#id_are_you_graduated_2').is(':checked')){
    $('.div_year').show();
    $('.div_study_year').hide();
    $('#id_study_year').val('');
    $('#id_study_year').removeAttr('required');
    $('#id_year_graduated').attr('required', 'required');
//    $('#div_id_institute label').text('Please select the Institute where graduated from');
    $('#div_id_institute_list label').text('Your Current University');
}
else{
    $('.div_year').hide();
    $('#id_year_graduated').val('');
    $('.div_study_year').show();
    $('#id_year_graduated').removeAttr('required');
    $('#id_study_year').attr('required', 'required');
//    $('#div_id_institute label').text('Your Selected Institute');
    $('#div_id_institute_list label').text('Please select the university where graduated from');
}
$(document).ready(function() {
   $('input[name="are_you_graduated"]').click(function() {
       if($(this).attr('id') == 'id_are_you_graduated_1') {
            $('.div_year').hide();
            $('#id_year_graduated').val('');
            $('.div_study_year').show();
            $('#id_year_graduated').removeAttr('required');
            $('#id_study_year').attr('required', 'required');
//            $('#div_id_institute label').text('Your Selected Institute');
            $('#div_id_institute_list label').text('Please select the university where graduated from');

       }
       else {
            $('.div_year').show();
            $('.div_study_year').hide();
            $('#id_study_year').val('');
            $('#id_study_year').removeAttr('required');
            $('#id_year_graduated').attr('required', 'required');
//            $('#div_id_institute label').text('Please select the Institute where graduated from');
            $('#div_id_institute_list label').text('Your Current University');

       }
   });
});

// Are you currently a tutor

if($('#id_are_you_currently_a_tutor_2').is(':checked')){
    privately_or_online();
    $('.div_have_experience_tutoring_agency_or_online').show();

    check_if_at_least_one_is_checked("tutoring_subject_list");
    check_if_at_least_one_is_checked("tutoring_in_level_list");
}
else{
    privately_or_online();
    $('.div_have_experience_tutoring_agency_or_online').hide();
    $('#id_have_experience_tutoring_agency_or_online option').removeAttr('selected');
    $('#id_have_experience_tutoring_agency_or_online option[value=0]').attr('selected', 'selected');

    set_custom_validity($('input[name="tutoring_subject_list"]')[0], '');
    set_custom_validity($('input[name="tutoring_in_level_list"]')[0], '');

}

function privately_or_online(){
    if($('#id_have_experience_tutoring_agency_or_online_2').is(':checked')){
         $('.div_name_of_agency_or_online_platforms').show();
    }
    else{
         $('.div_name_of_agency_or_online_platforms').hide();
         $('#id_name_of_agency_or_online_platforms').val('');

    }
}

$(document).ready(function() {
   $('input[name="are_you_currently_a_tutor"]').click(function() {
       if($(this).attr('id') == 'id_are_you_currently_a_tutor_2') {
           $('.div_have_experience_tutoring_agency_or_online').show();

           check_if_at_least_one_is_checked("tutoring_subject_list");
           check_if_at_least_one_is_checked("tutoring_in_level_list");
       }
       else {
            $("#id_have_experience_tutoring_agency_or_online_1").prop("checked", true);
            $('.div_have_experience_tutoring_agency_or_online').hide();
            $('#id_online_platform').val('');
            $('#id_hours_you_tutored').val('');
            $('#id_hours_you_commit_to_tutor').val('');
            privately_or_online();

            set_custom_validity($('input[name="tutoring_subject_list"]')[0], '');
            set_custom_validity($('input[name="tutoring_in_level_list"]')[0], '');

            $('input[name="tutoring_subject_list"]').prop('checked',false);
            $('input[name="tutoring_in_level_list"]').prop('checked',false);
            $('input[name="tutoring_with_list"]').prop('checked',false);
            $('input[name="languages_i_can_teach"]').prop('checked',false);
       }

   });
   $('input[name="have_experience_tutoring_agency_or_online"]').click(function() {
        privately_or_online();
   });
});

//privately_or_online();
//$('#id_have_experience_tutoring_agency_or_online').change(function(){
//
//});

// Check if at least one check box is field

function check_if_at_least_one_is_checked(input_name){
    const form = document.querySelector('#update-profile-form');
    if(Array.isArray(input_name)){
        query = ''
        for(var i = 0; i < input_name.length; i++) {
          query += "input[name='"+ input_name[i] +"']";
          query += (input_name.length - 1 == i ? '' : ',');
        }
    }
    else{
        query = "input[name='"+ input_name +"']";
    }
    const checkboxes = form.querySelectorAll(query);
    const checkboxLength = checkboxes.length;
    const firstCheckbox = checkboxLength > 0 ? checkboxes[0] : null;

    function init() {
        if (firstCheckbox) {
            for (let i = 0; i < checkboxLength; i++) {
                checkboxes[i].addEventListener('change', checkValidity);
            }
            checkValidity();
        }
    }

    function isChecked() {
        for (let i = 0; i < checkboxLength; i++) {
            if (checkboxes[i].checked) return true;
        }

        return false;
    }

    function checkValidity() {
        const errorMessage = !isChecked() ? 'At least one checkbox must be selected.' : '';
        firstCheckbox.setCustomValidity(errorMessage);
    }

    init();
}

// Content creation

if($('#id_experience_in_content_creation_2').is(':checked')){
    $('.div_about_content_creation').show();

}
else{
    $('.div_about_content_creation').hide();
}
$(document).ready(function() {
   $('input[name="experience_in_content_creation"]').click(function() {
       if($(this).attr('id') == 'id_experience_in_content_creation_1') {
            $('.div_about_content_creation').hide();

       }
       else {
            $('.div_about_content_creation').show();
       }
   });
});

// Employment

if($('#id_profile_made_visible_to_employers_2').is(':checked')){
    $('.div_about_yourself').show();
    $('#id_about_yourself').attr('required', 'required');
    $('#id_preferred_career_field').attr('required', 'required');
    $('#id_preferred_location').attr('required', 'required');
    $('#id_where_will_you_be_during_the_completion_of_your_internship').attr('required', 'required');
    $('#id_duration_of_internship').attr('required', 'required');
    $('#id_weekly_working_hours').attr('required', 'required');
    check_if_at_least_one_is_checked('skills_to_develop');

}
else{
    $('.div_about_yourself').hide();
    $('#id_about_yourself').removeAttr('required');
    $('#id_preferred_career_field').removeAttr('required');
    $('#id_preferred_location').removeAttr('required');
    $('#id_where_will_you_be_during_the_completion_of_your_internship').removeAttr('required');
    $('#id_duration_of_internship').removeAttr('required');
    $('#id_weekly_working_hours').removeAttr('required');
    set_custom_validity($('input[name="skills_to_develop"]')[0], '');


}
$(document).ready(function() {
   $('input[name="profile_made_visible_to_employers"]').click(function() {
       if($(this).attr('id') == 'id_profile_made_visible_to_employers_1') {
            $('.div_about_yourself').hide();
            $('#id_about_yourself').removeAttr('required');
            $('#id_about_yourself').val('');

            $('#id_preferred_career_field').removeAttr('required');
            $('#id_preferred_career_field').val(null).trigger('change');

            $('#id_preferred_location').removeAttr('required');
            $('#id_preferred_location').val(null).trigger('change');

            $('#id_where_will_you_be_during_the_completion_of_your_internship').removeAttr('required');
            $('#id_where_will_you_be_during_the_completion_of_your_internship').val(null).trigger('change');

            $('#id_duration_of_internship').removeAttr('required');
            $('#id_duration_of_internship').val(null).trigger('change');

            $('#id_weekly_working_hours').removeAttr('required');
            $('#id_weekly_working_hours').val(null).trigger('change');

            set_custom_validity($('input[name="skills_to_develop"]')[0], '');
            $('input[name="skills_to_develop"]').prop('checked',false);
       }
       else {
            $('.div_about_yourself').show();
            $('#id_about_yourself').attr('required', 'required');
            $('#id_preferred_career_field').attr('required', 'required');
            $('#id_preferred_location').attr('required', 'required');
            $('#id_where_will_you_be_during_the_completion_of_your_internship').attr('required', 'required');
            $('#id_duration_of_internship').attr('required', 'required');
            $('#id_weekly_working_hours').attr('required', 'required');
            check_if_at_least_one_is_checked('skills_to_develop');
       }
   });
});


// Foundation Provider

var value = $('#id_did_you_study_the_foundation_course_in_uk').val();
if(value == 1){
     $('.foundation_course_uk').show();
     $('#id_where_did_you_study').attr('required', 'required');
     $('#id_subject_foundation').attr('required', 'required');
}
else{
     $('.foundation_course_uk').hide();
     $('#id_where_did_you_study').val('');
     $('#id_subject_foundation').val('');
     $('#id_where_did_you_study').removeAttr('required');
     $('#id_subject_foundation').removeAttr('required');
}

$('#id_where_did_you_study').change(function(){
    var value = $('option:selected', this).text();
    if(value == "Other"){
         $('#div_id_foundation_provider').show();
        $('#id_foundation_provider').attr('required', 'required');


    }
    else{
         $('#div_id_foundation_provider').hide();
         $('#id_foundation_provider').removeAttr('required');

    }
});



var value = $('option:selected','#id_where_did_you_study').text();
if(value == "Other"){
     $('#div_id_foundation_provider').show();
    $('#id_foundation_provider').attr('required', 'required');


}
else{
     $('#div_id_foundation_provider').hide();
     $('#id_foundation_provider').removeAttr('required');

}

$('#id_did_you_study_the_foundation_course_in_uk').change(function(){
    var value = $(this).val();
    if(value == 1){
         $('.foundation_course_uk').show();
         $('#id_where_did_you_study').attr('required', 'required');
         $('#id_subject_foundation').attr('required', 'required');
    }
    else{
         $('.foundation_course_uk').hide();
         $('#id_where_did_you_study').val('');
         $('#id_subject_foundation').val('');
         $('#id_where_did_you_study').removeAttr('required');
         $('#id_subject_foundation').removeAttr('required');
    }
});


// AMBASSADOR

if($('#id_are_you_registered_as_an_ambassador_2').is(':checked')){
     $('.div_unibuddy').show();
}
else{
   $('.div_unibuddy').hide();
}

$('input[name="are_you_registered_as_an_ambassador"]').click(function(){
        if($(this).attr('id') == 'id_are_you_registered_as_an_ambassador_2') {
          $('.div_unibuddy').show();
        }
        else{
          $('.div_unibuddy').hide();
        }

  });

// DBS

if($('#id_dbs_check_2').is(':checked')){
     $('.dbs_check').show();
}
else{
     $('.dbs_check').hide();
     $('#id_dbs_certificate_type').val('');
     $('#id_dbs_Reference_no').val('');
     $('#id_dbs_date').val('');
     $('#id_dbs_certificate').val('');
}
$('input[name="dbs_check"]').click(function(){
        if($(this).attr('id') == 'id_dbs_check_2') {
            $('.dbs_check').show();
        }
        else{
             $('.dbs_check').hide();
             $('#id_dbs_certificate_type').val('');
             $('#id_dbs_Reference_no').val('');
             $('#id_dbs_date').val('');
             $('#id_dbs_certificate').val('');
        }
});


// Tutoring Subject

var value = $('#id_tutoring_subject').text();
        if(value == "Other"){
             $('#div_id_tutoring_subject_other').show();
        }
        else{
             $('#div_id_tutoring_subject_other').hide();
        }

$('#id_tutoring_subject').change(function(){
        var value = $('option:selected', this).text();
        if(value == "Other"){
             $('#div_id_tutoring_subject_other').show();
        }
        else{
             $('#div_id_tutoring_subject_other').hide();
        }
  });

// About me

  $(document).ready(function() {
  $('#div_id_about_me label').append('<span id="word_count"></span>');
  $("#id_about_me").on('keyup', function() {
    var words = 0;

    if ((this.value.match(/\S+/g)) != null) {
//      words = this.value.replace(/ /g,'').length;
      words = this.value.length;
    }

    if (words > 500) {
      this.value = this.value.substring(0, 500);
    }
    else {
      var word_count = 500-words
      $('#word_count').text("( Characters Left : " + word_count + " )");
    }
  });

  $('#div_id_about_content_creation label').append('<span id="word_count_content_creation"></span>');
  $("#id_about_content_creation").on('keyup', function() {
    var words = 0;

    if ((this.value.match(/\S+/g)) != null) {
      words = this.value.replace(/ /g,'').length;
    }

    if (words > 500) {
      this.value = this.value.substring(0, 500);
    }
    else {
      var word_count_content_creation = 500-words;
      $('#word_count_content_creation').text("( Char Left : " + word_count_content_creation + " )");
    }
  });

  $('#div_id_about_yourself label').append('<span id="word_count_content_creation_about_yourself"></span>');
  $("#id_about_yourself").on('keyup', function() {
    var words = 0;

    if ((this.value.match(/\S+/g)) != null) {
      words = this.value.replace(/ /g,'').length;
    }

    if (words > 500) {
      this.value = this.value.substring(0, 500);
    }
    else {
      var word_count_content_creation_about_yourself = 500-words;
      $('#word_count_content_creation_about_yourself').text("( Char Left : " + word_count_content_creation_about_yourself + " )");
    }
  });
});



// Save Button
if($('#id_consent1').is(':checked') && $('#id_consent2').is(':checked') && $('#id_consent3').is(':checked') && $('#id_consent4').is(':checked')) {
           $('#Button').removeClass('not-active');
}
else{
     $('#Button').addClass('not-active');
}
$("input[type=checkbox]").change(function(){
    if($('#id_consent1').is(':checked') && $('#id_consent2').is(':checked') && $('#id_consent3').is(':checked') && $('#id_consent4').is(':checked')) {
       $('#Button').removeClass('not-active');
    }
    else{
         $('#Button').addClass('not-active');
    }
});



// Institute Select
var country = $('#selected_studying_in_country').val();
var institute_name = $('#selected_institute_name').val();
if ( country != 'GB' ) {
    $(".institute_name").show();
    $(".institute_uk").hide();
    $("#email_type").text('');
    $('#id_institute_name').attr('required', 'required');
    $('#id_institute_list').removeAttr('required');
} else {
    $(".institute_name").hide();
    $(".institute_uk").show();
    $('#id_institute_name').removeAttr('required');
    $('#id_institute_list').attr('required', 'required');
}

// Assuming your dropdown element has an id of 'myDropdown'
var dropdown = $('#id_institute_list');
// Check if the value exists in the dropdown
if(institute_name){
    if (dropdown.find('option[value="' + institute_name + '"]').length) {
      // If the value exists, select it
      dropdown.val(institute_name).change();
    }else{
       dropdown.val('Other').change();
       $(".institute_name").show();
       $('#id_institute_name').removeAttr('required');
    }
}


$('#id_country').change(function () {
    var country = $(this).val();
    if (country != 'GB') {
      $(".institute_name").show();
      $(".institute_uk").hide();
      $("#email_type").text('');
      $('#id_institute_name').attr('required', 'required');
      $('#id_institute_list').removeAttr('required');
    } else {
      $(".institute_name").hide();
      $(".institute_uk").show();
      $('#id_institute_name').removeAttr('required');
      $('#id_institute_list').attr('required', 'required');
    }
});


var value = $('#id_institute_list').text();
if (value == "Other") {
  $('.institute_name').show();
  $('#id_institute_name').removeAttr('required');
}

$('#id_institute_list').change(function () {
  $('#id_institute_name').val('');
  var value = $('option:selected', this).text();
  if (value == "Other") {
     $('.institute_name').show();
     $('#id_institute_list').removeAttr('required');
     $('#id_institute_name').attr('required', 'required');
  }
  else {
     $('.institute_name').hide();
     $('#id_institute_name').removeAttr('required');
     $('#id_institute_list').attr('required', 'required');
  }
});



// Profile pic upload
function placeVal(x,y, width, height, rotation){
    $("#id_x").val(cropData["x"]);
    $("#id_y").val(cropData["y"]);
    $("#id_height").val(cropData["height"]);
    $("#id_width").val(cropData["width"]);
    $("#id_rotation").val(rotation_degree);
}
$('.dropzone').click(function(){ $("input[name='profile_pic']").trigger('click'); });
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
        else{
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
        if(rotation_degree==360){
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

    $('.cancel_btn').click(function(){
        $("input[name='profile_pic']").val('');
    })
})

// HR Section

$('#id_visa_start_date').datepicker({
    changeYear: true,
    dateFormat: "dd/mm/yy",
});
$('#id_visa_end_date').datepicker({
    changeYear: true,
    dateFormat: "dd/mm/yy",
});

if ($('#id_are_you_a_uk_national_1').is(':checked')) {
    $('.class_question_2').show();
    $('#visa_card-clear_id').attr('checked', false);
    $('#id_visa_start_date').attr('required', 'true');
    $('#id_visa_end_date').attr('required', 'true');
    $('input[name="visa_card"]').attr('required', 'true');
    $('label[for="id_visa_start_date"]').text('Visa start date*');
    $('label[for="id_visa_end_date"]').text('Visa end date*');
    $('label[for="id_visa_card"]').text('Visa card*');
}
else {
    $('#id_tier_4_visa_allow_you_to_work_in_uk_1').click();
    $('.class_question_2').hide();
    $('#question_2_options').hide();
    $('#id_visa_start_date').val('');
    $('#id_visa_end_date').val('');
    $('input[name="visa_card"]').val('');
    $('#visa_card-clear_id').attr('checked', true);
}

$('#id_are_you_a_uk_national_2').click(function () {
    if ($(this).is(':checked')) {
        $('#id_tier_4_visa_allow_you_to_work_in_uk_1').click();
        $('.class_question_2').hide();
        $('#question_2_options').hide();
        $('#id_visa_start_date').val('');
        $('#id_visa_end_date').val('');
        $('input[name="visa_card"]').val('');
        $('#visa_card-clear_id').attr('checked', true);
    }
    else {
        $('.class_question_2').show();
    }
})

$('#id_are_you_a_uk_national_1').click(function () {
    if ($(this).is(':checked')) {
        $('.class_question_2').show();
    }
    else {
        $('#id_tier_4_visa_allow_you_to_work_in_uk_1').click();
        $('.class_question_2').hide();
        $('#question_2_options').hide();
        $('#id_visa_start_date').val('');
        $('#id_visa_end_date').val('');
        $('input[name="visa_card"]').val('');
        $('#visa_card-clear_id').attr('checked', true);
        $('#id_visa_start_date').removeAttr('required');
        $('#id_visa_end_date').removeAttr('required');
        $('input[name="visa_card"]').removeAttr('required');
    }
})

function tier_4_visa_allow_you_to_work_in_uk_1(){
    if ($('#id_tier_4_visa_allow_you_to_work_in_uk_1').is(':checked')) {
        $('#question_2_options').hide();
        $('#id_visa_start_date').val('');
        $('#id_visa_end_date').val('');
        $('input[name="visa_card"]').val('');
        $('#visa_card-clear_id').attr('checked', true);
        $('#id_visa_start_date').removeAttr('required');
        $('#id_visa_end_date').removeAttr('required');
        $('input[name="visa_card"]').removeAttr('required');
    }
    else {
        $('#question_2_options').show();
        $('#visa_card-clear_id').attr('checked', false);
        $('#id_visa_start_date').attr('required', 'true');
        $('#id_visa_end_date').attr('required', 'true');
        $('input[name="visa_card"]').attr('required', 'true');
        $('label[for="id_visa_start_date"]').text('Visa start date*');
        $('label[for="id_visa_end_date"]').text('Visa end date*');
        $('label[for="id_visa_card"]').text('Visa card*');
    }
}
tier_4_visa_allow_you_to_work_in_uk_1();

$('#id_tier_4_visa_allow_you_to_work_in_uk_1').click(function () {
    tier_4_visa_allow_you_to_work_in_uk_1();
})
$('#id_tier_4_visa_allow_you_to_work_in_uk_2').click(function () {
    tier_4_visa_allow_you_to_work_in_uk_2();
})
function tier_4_visa_allow_you_to_work_in_uk_2(){
    if ($('#id_tier_4_visa_allow_you_to_work_in_uk_2').is(':checked')) {
        $('#question_2_options').show();
        $('#visa_card-clear_id').attr('checked', false);
        $('#id_visa_start_date').attr('required', 'true');
        $('#id_visa_end_date').attr('required', 'true');
        $('input[name="visa_card"]').attr('required', 'true');
        $('label[for="id_visa_start_date"]').text('Visa start date*');
        $('label[for="id_visa_end_date"]').text('Visa end date*');
        $('label[for="id_visa_card"]').text('Visa card*');
    }
    else {
        $('#question_2_options').hide();
        $('#id_visa_start_date').val('');
        $('#id_visa_end_date').val('');
        $('input[name="visa_card"]').val('');
        $('#visa_card-clear_id').attr('checked', true);
        $('#id_visa_start_date').removeAttr('required');
        $('#id_visa_end_date').removeAttr('required');
        $('input[name="visa_card"]').removeAttr('required');
    }
}
function are_you_uk_national(){
     var country_living_in = $("#id_currently_living_in_value").val();
     var country_studying_in = $("#id_studying_in_value").val();
     if (country_living_in == 'GB' && country_studying_in == 'GB'){
        $(".if_living_and_studying_uk_national").show();
        $(".if_not_living_and_studying_uk_national").hide();
     }
     else{
        $(".if_living_and_studying_uk_national").hide();
        $(".if_not_living_and_studying_uk_national").show();
        var country_living_in_label = $("#select2-id_currently_living_in-container").attr('title');
        if(country_living_in_label){
            $("label[for='id_eligible_to_work_in_country_living_in_0']").text('Are you eligible to work in ' + country_living_in_label + '?*');
        }
     }
     tier_4_visa_allow_you_to_work_in_uk_2();
}
are_you_uk_national();
$('#id_currently_living_in').on("change", function (e) {
    $("#id_tier_4_visa_allow_you_to_work_in_uk_1").prop("checked", true);
    are_you_uk_national();
});
$('#id_studying_in').on("change", function (e) {
    $("#id_tier_4_visa_allow_you_to_work_in_uk_1").prop("checked", true);
    are_you_uk_national();
});

$(document).ready(function() {
    are_you_uk_national();
});

function make_file_input_required(parent_element, field_name){
    if($(parent_element+" a").length ){
        $("input[name='" + field_name + "']").removeAttr('required');
    }
    else{
        $("input[name='" + field_name + "']").attr('required', 'required');
    }
}
make_file_input_required("#div_id_passport", "passport");

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

// Social Media Section
function check_if_at_least_n_filed_is_filled(id, number_of_fields_required, msg, input_filed){
    var social_field_values = $('#' + id).find(input_filed).filter(function() {
        return this.value !== "" && this.value !== "0";
    });
    if (social_field_values.length < number_of_fields_required) {
        $('#' + id).find(input_filed)[0].setCustomValidity(msg);
    }
    else{
        $('#' + id).find(input_filed)[0].setCustomValidity("");
    }
}
if( $('#social_media_section').length ){
    check_if_at_least_n_filed_is_filled('social_media_section', 1, "Please share at least one social media profile.", 'input');
    $('#social_media_section :input').change(function () {
        check_if_at_least_n_filed_is_filled('social_media_section', 1, "Please share at least one social media profile.", 'input');
    });
    check_if_at_least_one_is_checked(['follow_us_on_facebook', 'follow_us_on_instagram','follow_us_on_tiktok', 'follow_us_on_twitter', 'follow_us_on_linkedin', 'follow_us_on_youtube']);
}

// Questions field
if( $('#questions_section').length ){
    check_if_at_least_n_filed_is_filled('questions_section', 4, "Please answer at least 4 questions.", 'textarea');
    $('#questions_section').find('textarea').change(function () {
        check_if_at_least_n_filed_is_filled('questions_section', 4, "Please answer at least 4 questions.", 'textarea');
    });
}




// var country = $('#selected_studying_in_country').val();
// if (country){
//      $.ajax(
//      {
//          type:"GET",
//          url: '/application/get-institute',
//          data:{
//            country: country,
//            app:'',
//          },
//          success: function(response)
//          {
//            var instance = JSON.parse(response["country"]);
//            if(instance.length == 0){
//
//                $(".div_institute_name").show();
//                $("#div_id_institute").parent().closest('.div_where_did_you_study').hide();
//
//                $('#id_institute_name').attr('required', 'required');
//
//                $('#id_institute').removeAttr('required');
//
//            }else{
//                var fields = instance[0]["fields"];
//                var s;
//                                    s += '<option value="">Select Institute</option>';
//
//                for (var i = 0; i < instance.length; i++) {
//                    var selected = '';
//                    if ($("#id_institute").val() == instance[i].pk){
//                        selected = 'selected';
//                        }
//                    s += '<option value="' + instance[i].pk + '" '+ selected +'>' + instance[i].fields['institute_name'] + '</option>';
//                }
//                s += '<option value="">Other</option>';
//
//                 $(".div_institute_name").hide();
//                    $("#div_id_institute").parent().closest('.div_where_did_you_study').show();
//                    $('#id_institute_name').removeAttr('required');
//                      $('#id_institute').attr('required', 'required');
//
//            }
//               $("#id_institute").html(s);
//               if(instance.length > 0){
//               if ($('#id_institute_name').val() !== ''){
//                        $('#id_institute option:contains(Other)').prop('selected', true);
//                        $(".div_institute_name").show();
//
//                  }
//              }
//          }
//      })
//      }

//    $('#id_studying_in').change(function(){
//      var country = $(this).val();
//      $.ajax(
//      {
//          type:"GET",
//          url: '/application/get-institute',
//          data:{
//            country: country,
//            app:'',
//          },
//          success: function(response)
//          {
//            var instance = JSON.parse(response["country"]);
//            if(instance.length == 0){
//
//                $(".div_institute_name").show();
//                $("#div_id_institute").parent().closest('.div_where_did_you_study').hide();
//                $('#id_institute_name').attr('required', 'required');
//                $('#id_institute').removeAttr('required');
//
//            }else{
//                var fields = instance[0]["fields"];
//                var s;
//                s += '<option value="">Select Institute</option>';
//                for (var i = 0; i < instance.length; i++) {
//
//                    s += '<option value="' + instance[i].pk + '">' + instance[i].fields['institute_name'] + '</option>';
//
//                }
//                s += '<option value="">Other</option>';
//                 $(".div_institute_name").hide();
//                    $("#div_id_institute").parent().closest('.div_where_did_you_study').show();
//                    $('#id_institute_name').removeAttr('required');
//                    $('#id_institute').attr('required', 'required');
//            }
//               $("#id_institute").html(s);
//          }
//      })
//  });



//$('#id_institute').change(function(){
//        var value = $('option:selected', this).text();
//        if(value == "Other"){
//             $('.div_institute_name').show();
//             $('#id_institute').removeAttr('required');
//             $('#id_institute_name').attr('required', 'required');
//
//        }
//        else{
//             $('.div_institute_name').hide();
//               $('#id_institute_name').removeAttr('required');
//              $('#id_institute').attr('required', 'required');
//
//        }
//  });