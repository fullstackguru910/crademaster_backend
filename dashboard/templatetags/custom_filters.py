from django import template

register = template.Library()

@register.filter
def add_class(value, class_name):
    return value.as_widget(attrs={'class': class_name})


@register.filter
def seconds_to_hms(seconds):
    seconds = int(seconds)
    if not seconds:
        return ""
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = seconds % 60
    return f"{hours} hrs {minutes} mins {seconds} sec"
