$('#id_country').select2({
placeholder: 'Choose country',
searchInputPlaceholder: 'Search'
});
$('#id_nationality').select2({
placeholder: 'Choose country',
searchInputPlaceholder: 'Search'
});
$('#id_user_type').select2({
placeholder: 'Choose user type',
searchInputPlaceholder: 'Search'
});
$('#id_institute_list').select2({
   placeholder: 'Choose Institute',
   searchInputPlaceholder: 'Search',
});

$(":password").attr("pattern", "(?=.*[a-z])(?=.*[0-9]).{8,}").attr("title", "Must contain at least one number and one uppercase and lowercase letter, and at least 8 or more characters");

// Email type
$('#id_email').append('<small id="hint_id_password2" class="form-text text-muted">Enter the same password as before, for verification.</small>');

document.getElementById('link').value = window.location.protocol + "//" + window.location.hostname + (window.location.port ? ':' + window.location.port : '');
// document.getElementById('link2').value = window.location.protocol + "//" + window.location.hostname + (window.location.port ? ':' + window.location.port : '');

$("#exampleCheck1").change(function () {
  $('#register_student').toggleClass('not-active');
});
$("#exampleCheck2").change(function () {
  $('#register_mentor').toggleClass('not-active');
});
$("#exampleCheck3").change(function () {
  $('#google_signup').toggleClass('not-active');
});
$(".institute_uk").hide();
$('.institute_name').show();

// Country selection
//function check_country() {
//  if ($("#id_country option:selected").val() !== 'GB') {
//     $("#hint_id_email").hide();
//  }
//  else {
//     $("#hint_id_email").show();
//  }
//}
//check_country();
//$('#id_country').on('change', function () {
//  console.log($(this).val());
//  check_country();
//});

// Institute Select

var country = $('#id_country').val();
//if (country !== '') {
//  $.ajax(
//     {
//        type: "GET",
//        url: '/application/get-institute',
//        data: {
//           country: country,
//           app: '',
//        },
//        success: function (response) {
//           var instance = JSON.parse(response["country"]);
//           if (instance.length == 0) {
//              $(".institute_name").show();
//              $(".institute_uk").hide();
//              $("#email_type").text('');
//              $('#id_institute_name').attr('required', 'required');
//              $('#id_institute_list').removeAttr('required');
//
//           } else {
//              var fields = instance[0]["fields"];
//              var s;
//              s += '<option value="">Select Institute</option>';
//              for (var i = 0; i < instance.length; i++) {
//                 s += '<option value="' + instance[i].pk + '">' + instance[i].fields['institute_name'] + '</option>';
//              }
//              s += '<option value="other">Other</option>';
//              $(".institute_name").hide();
//              $(".institute_uk").show();
//              $('#id_institute_name').removeAttr('required');
//              $('#id_institute_list').attr('required', 'required');
//           }
//           $("#id_institute_list").html(s);
//        }
//     })
//}

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

//$('#id_country').change(function () {
//  var country = $(this).val();
//  $.ajax(
//     {
//        type: "GET",
//        url: '/application/get-institute',
//        data: {
//           country: country,
//           app: '',
//        },
//        success: function (response) {
//           var instance = JSON.parse(response["country"]);
//           if (instance.length == 0) {
//              $(".institute_name").show();
//              $(".institute_uk").hide();
//              $("#email_type").text('');
//              $('#id_institute_name').attr('required', 'required');
//              $('#id_institute_list').removeAttr('required');
//           } else {
//              var fields = instance[0]["fields"];
//              var s;
//              s += '<option value="">Select Institute</option>';
//              for (var i = 0; i < instance.length; i++) {
//                 s += '<option value="' + instance[i].pk + '">' + instance[i].fields['institute_name'] + '</option>';
//              }
//              s += '<option value="other">Other</option>';
//
//              $(".institute_name").hide();
//              $(".institute_uk").show();
//              $('#id_institute_name').removeAttr('required');
//              $('#id_institute_list').attr('required', 'required');
//           }
//           $("#id_institute_list").html(s);
//        }
//     })
//});

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

// Check How did you hear about us other field
$('.how_did_you_hear_about_us_other').hide();
var value = $("select[name='how_did_you_hear_about_us']").text();
if (value == "Other") {
  $('.how_did_you_hear_about_us_other').show();

}

$("select[name='how_did_you_hear_about_us']").change(function () {
  $("input[name='how_did_you_hear_about_us_other']").val('');
  var value = $('option:selected', this).text();
  if (value == "Other") {
     $('.how_did_you_hear_about_us_other').show();
     $("select[name='how_did_you_hear_about_us']").removeAttr('required');
     $("input[name='how_did_you_hear_about_us_other']").attr('required', 'required');
  }
  else {
     $('.how_did_you_hear_about_us_other').hide();
     $("input[name='how_did_you_hear_about_us_other']").removeAttr('required');
     $("select[name='how_did_you_hear_about_us']").attr('required', 'required');
  }
});

// Check if email already exists
function check_email_exists(form_id) {
  if ($(form_id + ' #error_1_id_email').length) {
  }
  else {
     $("<span class='invalid-feedback text-danger' id='error-email'><strong>This email is taken. Try another</strong></span>").insertAfter(form_id + ' #id_email');
  }
  $(form_id + ' #id_email').on('input', function () {
     var email = $(this).val();
     $.ajax(
        {
           type: "GET",
           url: '/get-email-exists',
           data: {
              email: email,
           },
           success: function (response) {
              var email_exist = JSON.parse(response["email_exist"]);
              if (email_exist) {
                 $(form_id + ' #error-email').show();
                 $(form_id + ' #id_email')[0].setCustomValidity("This email is taken. Try another.");
              }
              else {
                 $(form_id + ' #error-email').hide();
                 $(form_id + ' #id_email')[0].setCustomValidity("");
              }
           }
        })
  });

}
check_email_exists('#pills-Student');
check_email_exists('#pills-Mentor');

// Check if two password field are equal
// function check_password_match(form_id) {
//   $(form_id + ' input[name=password2]').keyup(function () {
//      if ($(form_id + ' input[name=password1]').val() === $(this).val()) {
//         this.setCustomValidity('');
//      } else {
//         this.setCustomValidity('Passwords must match');
//      }
//   });
// }
// check_password_match('#pills-Student');
// check_password_match('#pills-Mentor');

// Show password
$("body").on('click', '.toggle-password', function() {
   $(this).toggleClass("eye eye-off");
   let password1 = $("input[name='password1']");
   if (password1.attr("type") === "password") {
       password1.attr("type", "text");
       $(this).attr("class", "feather feather-eye-off eye-close toggle-password");
   } else {
       password1.attr("type", "password");
       $(this).attr("class", "feather feather-eye eye-open toggle-password");
   }

   let password2 = $("input[name='password2']");
   if (password2.attr("type") === "password") {
       password2.attr("type", "text");
       $(this).attr("class", "feather feather-eye-off eye-close toggle-password");
   } else {
       password2.attr("type", "password");
       $(this).attr("class", "feather feather-eye eye-open toggle-password");
   }
});




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
           select_default_country_select2('id_country', response.country);
       }
   }
//    console.log(JSON.stringify(response, null, 4));
}, "jsonp");

// Onclick scroll to form
$("#pills-applicant-tab").click(function() {
    $('html,body').animate({
        scrollTop: $("#mentor-form-tab").offset().top},
        'slow');
});
$("#pills-mentor-tab").click(function() {
    $('html,body').animate({
        scrollTop: $("#applicant-form-tab").offset().top},
        'slow');
});
$("#pills-tab a").click(function(){
  $("select[name='how_did_you_hear_about_us']").val('').change();
});