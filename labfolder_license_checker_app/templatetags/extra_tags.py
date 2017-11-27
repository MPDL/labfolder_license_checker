import datetime
from dateutil.relativedelta import relativedelta
from django import template
import logging
logger = logging.getLogger(__name__)

register = template.Library()

@register.simple_tag
def active_users_by_date(instance, date_from, date_to):
    return instance.active_users_by_date(date_from, date_to)

@register.simple_tag
def date_older(date, months):
    # Get end of last month as to_date
    if (date):
        month_now = datetime.datetime.now().replace(day=1)
        month_past = month_now + relativedelta(months=-months)
        return date < month_past.date()


