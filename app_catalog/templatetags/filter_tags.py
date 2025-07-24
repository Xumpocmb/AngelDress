from django import template

register = template.Library()


@register.simple_tag
def remove_filter(request, filter_name, filter_value):
    query_dict = request.GET.copy()
    current_values = query_dict.getlist(filter_name)

    if str(filter_value) in current_values:
        current_values.remove(str(filter_value))
        query_dict.setlist(filter_name, current_values)

    return query_dict.urlencode()


@register.filter
def get_item(queryset, item_id):
    """Фильтр для получения объекта из QuerySet по ID"""
    try:
        return queryset.get(id=item_id)
    except:
        return None