var notify_badge_class;
var notify_menu_class;
var notify_api_url;
var notify_fetch_count;
var notify_unread_url;
var notify_mark_all_unread_url;
var notify_refresh_period = 15000;
var consecutive_misfires = 0;
var registered_functions = [];

function fill_notification_badge(data) {
    var badges = document.getElementsByClassName(notify_badge_class);
    if (badges) {
        for(var i = 0; i < badges.length; i++){
            badges[i].innerHTML = data.unread_count;
        }
    }
}

function fill_notification_list(data) {
    var menus = document.getElementsByClassName(notify_menu_class);
    
    // if(menus.length==1){
    //     $("p").html('<h5>You have no unread notifications!</h5>');
    // }
    if (menus) {
        var messages = data.unread_list.map(function (item) {
            // console.log(item.new_time);
            var message = "";
            var url_name = "#";
            if(typeof item.verb !== 'undefined'){
                message = message + " " + item.verb;
            }
            if(item.description !== '#'){
                url_name = item.description;
            }
            var read_url = "/inbox/notifications/mark-as-read/" + item.slug;
            // return '<div class="list-group-item list-group-item-action flex-column align-items-start active"><div class="d-flex w-100 justify-content-between"><a href="'
            //         + url_name +'"><h5 class="mb-1">' + message +'</h5></a><small class="text-muted"><a href="'+ read_url +'">Mark as Read </a></small></div><small class="text-muted">' + item.timestamp +'</small></div>'
            return '<div class="alert alert-block alert-'
                    + item.level +'"><a class="close pull-right" href="'
                    + read_url +'"><i class="icon-close"></i></a><h6><i class="icon-mail-alt"></i><a href="'
                    + url_name +'">' + item.new_time +'</a></h6></div>'
                }).join('')

        for (var i = 0; i < menus.length; i++){
            menus[i].innerHTML = messages;
        }
    }
}

function register_notifier(func) {
    registered_functions.push(func);
}

function fetch_api_data() {
    if (registered_functions.length > 0) {
        //only fetch data if a function is setup
        var r = new XMLHttpRequest();
        r.addEventListener('readystatechange', function(event){
            if (this.readyState === 4){
                if (this.status === 200){
                    consecutive_misfires = 0;
                    var data = JSON.parse(r.responseText);
                    for(var i = 0; i < registered_functions.length; i++) {
                       registered_functions[i](data);
                    }
                }else{
                    consecutive_misfires++;
                }
            }
        })
        r.open("GET", notify_api_url+'?max='+notify_fetch_count, true);
        r.send();
    }
    if (consecutive_misfires < 10) {
        setTimeout(fetch_api_data,notify_refresh_period);
    } else {
        var badges = document.getElementsByClassName(notify_badge_class);
        if (badges) {
            for (var i = 0; i < badges.length; i++){
                badges[i].innerHTML = "!";
                badges[i].title = "Connection lost!"
            }
        }
    }
}

setTimeout(fetch_api_data, 1000);
