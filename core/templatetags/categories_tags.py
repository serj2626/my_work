from django import template
from core.models import Category

register = template.Library()

#
# @register.simple_tag()
# def get_categories():
#     return Category.objects.all()


@register.inclusion_tag('include/list_categories.html')
def show_categories():
    cats = Category.objects.all()
    return {"categories": cats}
