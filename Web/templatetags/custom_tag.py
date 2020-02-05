from django import template,conf

register = template.Library()
from django.utils.safestring import mark_safe

@register.simple_tag
def str_group_host(group_host):
    str_group_name = str(group_host)+'xxx'
    return str_group_name

# 获取DATA数据中的Json文件
@register.simple_tag
def get_command_history_josn_path(id):
    print("进入get_command_history_josn_path标签")
    path = "%s%sdata/%s/command_history" % (conf.settings.BASE_DIR,conf.settings.STATIC_URL,id)
    print(path)
    return path