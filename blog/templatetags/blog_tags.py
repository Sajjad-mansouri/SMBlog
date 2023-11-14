from django import template
from blog.models import Category

register = template.Library()

@register.inclusion_tag("partials/_navbar.html")
def navbar():
	return {'category':Category.objects.filter(status=True)}
