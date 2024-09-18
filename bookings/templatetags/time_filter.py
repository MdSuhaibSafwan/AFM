from django import template
from datetime import datetime

register = template.Library()


@register.filter
def gc_time(td):
    time = datetime.strptime(td, "%H:%M").time()
    return time.strftime("%H%M%S")