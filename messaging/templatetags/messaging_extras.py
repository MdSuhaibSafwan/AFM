import datetime
from django.utils.html import format_html
from AFM.utils import get_current_request
from django import template
from messaging.models import Messaging
from django.template.defaultfilters import stringfilter
from django.utils.safestring import mark_safe
from django.utils.html import urlize as urlize_impl

register = template.Library()


@register.filter
def get_user_live_unread_messages_count(value):
    request = get_current_request()
    user = request.user
    if not user:
        return ''
    unread_msg = Messaging.objects.filter(sender__slug=value,
                                          receiver=request.user,
                                          read=False).exclude(sender=request.user).count()
    if unread_msg > 0:
        html = "<span class='unread_msgs' user_slug='{user_slug}' >{unread}</span>".format(user_slug=value,
                                                                                           unread=unread_msg
                                                                                           )
    else:
        html = "<span class='unread_msgs' user_slug='{user_slug}' style='display: none;'>{unread}</span>".format(
            user_slug=value,
            unread=unread_msg
        )
    return format_html(html)


@register.filter
def get_message_receive_date(id):
    msg_object = Messaging.objects.get(id=id)
    if Messaging.objects.filter(created_at__year=msg_object.created_at.year,
                                created_at__month=msg_object.created_at.month,
                                created_at__day=msg_object.created_at.day,
                                sender__in=[msg_object.sender, msg_object.receiver],
                                receiver__in=[msg_object.sender, msg_object.receiver]).order_by(
                                'created_at').first().id == id:
        delta = datetime.date.today() - msg_object.created_at.date()
        if delta.days == 0:
            days_to_go = 'Today'
        elif delta.days == 1:
            days_to_go = 'A day ago'
        else:
            days_to_go = str(delta.days) + " days ago"
        html = "<label class='az-chat-time'><span>{date}</span></label>".format(date=days_to_go)
        return format_html(html)
    return ''


@register.filter
def print_options(x):
    if x:
        str = ''
        for i in x:
            str = str + i.option + '<br> '
        return format_html(str[:-2])
    return '--'

# @register.filter(is_safe=True, needs_autoescape=True)
# @stringfilter
# def urlize_target_blank(value):
#     return mark_safe(urlize_impl(value, None, True, autoescape=None).replace('<a', '<a target="_blank"'))

@register.filter(is_safe=True)
def url_target_blank(text):
    return mark_safe(text.replace('<a ', '&nbsp;<a target="_blank" ').replace('</a>', '</a>&nbsp;'))

