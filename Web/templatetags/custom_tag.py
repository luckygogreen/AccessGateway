from django import template

register = template.Library()
from django.utils.safestring import mark_safe

@register.simple_tag
def str_group_host(group_host):
    str_group_name = str(group_host)+'xxx'
    return str_group_name
