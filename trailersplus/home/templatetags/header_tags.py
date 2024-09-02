from django import template

register = template.Library()


@register.filter
def remove_locale(path):
    path_parts = path.split("/")
    path_parts.pop(0)
    if path_parts[0].lower() in ("en", "es"):
        path_parts.pop(0)
    return "/".join(path_parts)


@register.filter
def with_locale(path, lang):
    return f'{lang}/{remove_locale(path)}'
