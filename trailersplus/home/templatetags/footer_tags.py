from django import template
from ..models import Footer

register = template.Library()


@register.inclusion_tag("templates/includes/footer.html", takes_context=True)
def get_footer(context):
    return {
        "footers": Footer.objects.all(),
        "request": context["request"],
    }
