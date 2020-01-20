from django import template

register = template.Library()
from django.utils.safestring import mark_safe


@register.simple_tag
def show_hostlist(group_host, hostlist_with_group):
    show_hostlist_html = ''
    for single_host in hostlist_with_group[group_host]:
        host_id = single_host[0]
        host_name = single_host[1]
        host_ip = single_host[2]
        show_hostlist_html += '''<tr>
                                            <td class="bs-checkbox ">
                                                 <input name="%sxxx" type="checkbox" id="%s" />
                                            </td>
                                            <td>%s</td>
                                            <td>%s</td>
                                            <td>%s</td>
                                        </tr>''' % (group_host, host_id, host_id, host_name, host_ip)
    return mark_safe(show_hostlist_html)


@register.simple_tag
def str_group_host(group_host):
    str_group_name = str(group_host)+'xxx'
    return str_group_name
