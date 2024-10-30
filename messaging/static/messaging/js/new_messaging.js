$("input[name='msg']").keyup(function (event) {
    if (event.keyCode === 13) {
        $("#msg-send-button").click();
    }
});

function urlify(text) {
    var urlRegex = /(((https?:\/\/)|(www\.))[^\s]+)/g;
    return text.replace(urlRegex, function (url) {
        return '&nbsp;<a href="' + url + '" target="_blank">' + url + '</a>&nbsp;';
    })
    // or alternatively
    // return text.replace(urlRegex, '<a href="$1">$1</a>')
}


$("#msg-send-button").click(function () {
    let msg = $("input[name='msg']").val();
    let wordArray = ['visa','visas','fee','fees','scholarship','scholarships','immigration','immigrations', 'discount','discounts']
    
    var sender_slug = JSON.parse(document.getElementById('sender_slug').textContent);
    let receiver_slug = $(this).attr('data-receiver');

    if (wordArray.some(word => msg.includes(word)) ) {
        console.log("keyword caught in message")

        $.ajax(
            {
                type: "GET",
                url: "/message/send-ajax-message-with-keyword/",
                data: {
                    msg: msg,
                    sender_slug: sender_slug,
                    receiver_slug: receiver_slug,
                    },
                success: function (response) {
                    let msg_send_status = JSON.parse(response["msg_send_status"]);
                    let msg_id = JSON.parse(response["msg_id"]);
                    let message = JSON.parse(response["msg"]);

                    if (msg_send_status) {
                        
                        let msg_html = "<div class='media flex-row-reverse'>" +
                                        "<div class='media-body'>" +
                                        "<div class='az-msg-wrapper unread-msg' data-id='" + msg_id + "'>" +
                                        message +
                                        "<svg xmlns='http://www.w3.org/2000/svg' width='24' height='24'" +
                                        "viewBox='0 0 24 24' fill='none' stroke='currentColor' stroke-width='2'" +
                                        "stroke-linecap='round' stroke-linejoin='round'" +
                                        "class='feather feather-check fs-dark'><polyline points='20 6 9 17 4 12'>" +
                                        "</polyline>" +
                                        "</svg>" +
                                        "<svg xmlns='http://www.w3.org/2000/svg' width='24' height='24'" +
                                        "viewBox='0 0 24 24' fill='none' stroke='currentColor' stroke-width='2'" +
                                        "stroke-linecap='round' stroke-linejoin='round'" +
                                        "class='feather feather-check fs-dark right-0'><polyline points='20 6 9 17 4 12'>" +
                                        "</polyline>" +
                                        "</svg>" +
                                        "</div>" +
                                        "</div>" +
                                        "</div>";
                        
                        // let word_html = "<div class='media reverse'>" +
                        //             "<div class='media-body'>" +
                        //             "<div class='az-msg-wrapper unread-msg' style='background-color: #f7d3df;'>" +
                        //             "Sorry, I'm unable to advise on visas, specific fees, etc. AP will assist with this after you have applied." +
                        //             "</div>" +
                        //             "</div>" +
                        //             "</div>";
                        
                       
                        $(msg_html).appendTo('#azChatBody .content-inner'); 
                        // $(word_html).appendTo('#azChatBody .content-inner');           
                        console.log("Default message displayed - Word found in message");
                        $("input[name='msg']").val('');
                        $("input[name='msg']").focus();
                        $("#azChatBody").animate({ scrollTop: $("#azChatBody")[0].scrollHeight }, 0);
                    
                    } else {
                        alert('Message not sent !!');
                    }
                }
            });
    }else{
        console.log("keyword is absent")
        if (msg) {
            $.ajax(
                {
                    type: "GET",
                    url: "/message/send-ajax-message/",
                    data: {
                        msg: msg,
                        receiver_slug: receiver_slug,
                        },
                    success: function (response) {
                        let msg_send_status = JSON.parse(response["msg_send_status"]);
                        let msg_id = JSON.parse(response["msg_id"]);
                        let message = JSON.parse(response["msg"]);
    
                        if (msg_send_status) {
                            let msg_html = "<div class='media flex-row-reverse'>" +
                                        "<div class='media-body'>" +
                                        "<div class='az-msg-wrapper unread-msg' data-id='" + msg_id + "'>" +
                                        message +
                                        "<svg xmlns='http://www.w3.org/2000/svg' width='24' height='24'" +
                                        "viewBox='0 0 24 24' fill='none' stroke='currentColor' stroke-width='2'" +
                                        "stroke-linecap='round' stroke-linejoin='round'" +
                                        "class='feather feather-check fs-dark'><polyline points='20 6 9 17 4 12'>" +
                                        "</polyline>" +
                                        "</svg>" +
                                        "<svg xmlns='http://www.w3.org/2000/svg' width='24' height='24'" +
                                        "viewBox='0 0 24 24' fill='none' stroke='currentColor' stroke-width='2'" +
                                        "stroke-linecap='round' stroke-linejoin='round'" +
                                        "class='feather feather-check fs-dark right-0'><polyline points='20 6 9 17 4 12'>" +
                                        "</polyline>" +
                                        "</svg>" +
                                        "</div>" +
                                        "</div>" +
                                        "</div>";
    
                            $(msg_html).appendTo('#azChatBody .content-inner');
                            console.log("Message displayed......");
                            $("input[name='msg']").val('');
                            $("input[name='msg']").focus();
                            $("#azChatBody").animate({ scrollTop: $("#azChatBody")[0].scrollHeight }, 0);
                        
                        } else {
                            alert('Message not sent !!');
                        }
                    }
                });
        } else {
            alert('Please Type Message!!');
        };
    };

    
});

function update_messages() {
    var receiver_slug = $("#msg-send-button").attr('data-receiver');
    $.ajax(
        {
            type: "GET",
            url: "/message/update-new-messages",
            data: {
                receiver_slug: receiver_slug,
            },
            success: function (response) {
                var unread_msgs = response["unread_msgs"];
                if (unread_msgs) {
                    let msg_html = null
                    let view_button = null
                    if (response["user_type"] === "Applicant") {
                        view_button = "<div class='row'>" +
                            "<a class='btn btn-info w-50 ml-3 text-white'" +
                            "href='/booking/confirm/" + response["appointment_id"] + "/'>View</a>" +
                            "</div>"
                    }
                    if (response["appointment_id"]) {
                        msg_html =
                            "<div class='media reverse'>" +
                            "<div class='media-body'>" +
                            "<div class='az-msg-wrapper'>" +
                            "<div class='row' style='width: 34rem'>" +
                            "<div class='col-lg-8 col-md-8 col-sm-8 '>" +
                            "<div >" +
                            "<h6 class='service-label'>Session Date</h6>" +
                            "<p class='service-info' id='datePara'>" + response["appointment_date"] + "</p>" +
                            "</div>" +
                            "<div >" +
                            "<h6 class='service-label'>Session Time</h6>" +
                            "<div class='service-info'>" +
                            "<p>" + response["appointment_from_time"] + " - " + response["appointment_to_time"] +
                            "<span style='color: red;'>(" + response["appointment_booker_timezone"] + " Time)</span></p>" +
                            "</div>" +
                            "</div>" +
                            "<div >" +
                            "<h6 class='service-label'>Alumni ID</h6>" +
                            "<p class='service-info'>" + response["appointment_provider_slug"] + "</p>" +
                            "</div>" +
                            "</div>" +
                            "<div class='col-lg-4 col-md-4 col-sm-4 '>" +
                            "<div >" +
                            "<h6 class='service-label'>Service</h6>" +
                            "<p class='service-info'>" + response["appointment_services_title"] + "</p>" +
                            "</div>" +
                            "<div >" +
                            "<h6 class='service-label'>Service Duration</h6>" +
                            "<p class='service-info'>" + response["appointment_duration_minutes"] + " minutes</p>" +
                            "</div>" +
                            "<div >" +
                            "<h6 class='service-label'>Cost Of Session</h6>" +
                            "<p class='service-info'>" +
                            "FREE!" +
                            "</p>" +
                            "</div>" +
                            "</div>" +
                            "</div>" + view_button +
                            "</div>" +
                            "</div>" +
                            "</div>";
                    } else {
                        msg_html =
                            "<div class='media reverse'>" +
                            "<div class='media-body'>" +
                            "<div class='az-msg-wrapper'>" +
                            unread_msgs +
                            "</div>" +
                            "</div>" +
                            "</div>";
                    }
                    $(msg_html).appendTo('#azChatBody .content-inner');
                    $("#azChatBody").animate({ scrollTop: $("#azChatBody")[0].scrollHeight }, 0);
                }
            }
        })
}
function check_msg_read_unread() {
    $('div.unread-msg').each(function () {
        msg_id = $(this).attr('data-id');
        $.ajax(
            {
                type: "GET",
                url: "/message/check-msg-read-unread",
                data: {
                    msg_id: msg_id,
                },
                success: function (response) {
                    var msg_read_status = response["msg_read_status"];
                    if (msg_read_status) {
                        $("div[data-id='" + msg_id + "']").children('.feather-check').addClass('fs-blue');
                        $("div[data-id='" + msg_id + "']").removeClass('unread-msg');
                    }
                }
            })
    });
}

var myInterval_check_msg_read_unread = setInterval(check_msg_read_unread, 10000);
var myInterval_update_messages = setInterval(update_messages, 8000);

$("#azChatBody").animate({ scrollTop: $("#azChatBody")[0].scrollHeight }, 0);
$("html, body").animate({ scrollTop: $(document).height() }, 0);
$(function () {
    'use strict'
    if (window.matchMedia('(min-width: 992px)').matches) {

        const azChatBody = new PerfectScrollbar('#azChatBody', {
            suppressScrollX: true
        });
    }
    $('.az-chat-list .media').on('click touch', function () {
        $(this).addClass('selected').removeClass('new');
        $(this).siblings().removeClass('selected');

        // if(window.matchMedia('(max-width: 991px)').matches) {
        $('body').addClass('az-content-body-show');
        $('html body').scrollTop($('html body').prop('scrollHeight'));
        // }
    });
});
$(function () {
    $('[data-toggle="tooltip"]').tooltip()
    $(".add-booking-link").click(function () {
        $("input[name='msg']").val($("input[name='msg']").val() + $(this).attr('data-booking-link'));
        $("input[name='msg']").focus();
    });
    $(document).click(function (e) {
        if (!$(e.target).is('.card-body')) {
            $('.collapse').collapse('hide');
        }
    });
});
var $viewportMeta = $('meta[name="viewport"]');
$('input, select, textarea').bind('focus blur', function (event) {
    $viewportMeta.attr('content', 'width=device-width,initial-scale=1,maximum-scale=' + (event.type == 'blur' ? 10 : 1));
});

// Hide sticky menu on keyboard for mobile

function onKeyboardOnOff(isOpen) {
    // Write down your handling code
    if (isOpen) {
        $(".height").addClass('h-148');
        $(".az-chat-footer").addClass('bottom-0');
        $(".floating-menu-area").addClass('float-d-none');
        $("#azChatBody").animate({ scrollTop: $("#azChatBody")[0].scrollHeight }, 0);
    } else {
        $(".height").removeClass('h-148');
        $(".az-chat-footer").removeClass('bottom-0');
        $(".floating-menu-area").removeClass('float-d-none');
    }
}

var originalPotion = false;
$(document).ready(function () {
    if (originalPotion === false) originalPotion = $(window).width() + $(window).height();
});

/**
 * Determine the mobile operating system.
 * This function returns one of 'iOS', 'Android', 'Windows Phone', or 'unknown'.
 *
 * @returns {String}
 */
function getMobileOperatingSystem() {
    var userAgent = navigator.userAgent || navigator.vendor || window.opera;

    // Windows Phone must come first because its UA also contains "Android"
    if (/windows phone/i.test(userAgent)) {
        return "winphone";
    }

    if (/android/i.test(userAgent)) {
        return "android";
    }

    // iOS detection from: http://stackoverflow.com/a/9039885/177710
    if (/iPad|iPhone|iPod/.test(userAgent) && !window.MSStream) {
        return "ios";
    }

    return "";
}

function applyAfterResize() {

    if (getMobileOperatingSystem() != 'ios') {
        if (originalPotion !== false) {
            var wasWithKeyboard = $('body').hasClass('view-withKeyboard');
            var nowWithKeyboard = false;

            var diff = Math.abs(originalPotion - ($(window).width() + $(window).height()));
            if (diff > 100) nowWithKeyboard = true;

            $('body').toggleClass('view-withKeyboard', nowWithKeyboard);
            if (wasWithKeyboard != nowWithKeyboard) {
                onKeyboardOnOff(nowWithKeyboard);
            }
        }
    }
}

$(document).on('focus blur', 'select, textarea, input[type=text], input[type=date], input[type=password], input[type=email], input[type=number]', function (e) {
    var $obj = $(this);
    var nowWithKeyboard = (e.type == 'focusin');
    $('body').toggleClass('view-withKeyboard', nowWithKeyboard);
    onKeyboardOnOff(nowWithKeyboard);
});

$(window).on('resize orientationchange', function () {
    applyAfterResize();
});