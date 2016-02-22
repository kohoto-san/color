from django import template
from django.template import defaultfilters

from datetime import date, datetime

register = template.Library()

@register.filter(expects_localtime=True)
def days_since(value, arg=None):
    """
    For date values that are tomorrow, today or yesterday compared to
    present day returns representing string. Otherwise, returns a string
    formatted according to settings.DATE_FORMAT.
    """
    try:
        tzinfo = getattr(value, 'tzinfo', None)
        value = date(value.year, value.month, value.day)
    except AttributeError:
        # Passed value wasn't a date object
        return value
    except ValueError:
        # Date arguments out of range
        return value
    today = datetime.now(tzinfo).date()
    delta = value - today
    if delta.days == 0:
        return _('today')
    elif delta.days == 1:
        return _('tomorrow')
    elif delta.days == -1:
        return _('yesterday')
    return defaultfilters.date(value, arg)


"""
# http://stackoverflow.com/questions/6494921/how-to-display-x-days-ago-type-time-using-humanize-in-django-template
# http://stackoverflow.com/questions/24818768/django-built-in-timesince-filter-to-show-only-days
@register.filter(expects_localtime=True)
def days_since(value, arg=None):

    try:
        tzinfo = getattr(value, 'tzinfo', None)
        value = date(value.year, value.month, value.day)
    except AttributeError:
        # Passed value wasn't a date object
        return value
    except ValueError:
        # Date arguments out of range
        return value
    today = datetime.now(tzinfo).date()
    delta = value - today

    if delta.days == 0:
        small_delta = True
        day_str = _('Today')
    elif delta.days == -1:
        small_delta = True
        day_str = _('Yesterday')
    elif delta.days < -1:
        small_delta = False
        day_str = _('Days')

    if small_delta:
        return "%s" % (day_str)
    else:
        return "%s %s" % (abs(delta.days), day_str)
"""
