from django import template
from blog.models import Category

register = template.Library()

@register.inclusion_tag("partials/_navbar.html",takes_context=True)
def navbar(context):
	request=context['request']
	return {
	'category':Category.objects.filter(status=True),
	'request':request
	}

@register.inclusion_tag("partials/_pagination.html",takes_context=True)
def pagination(context):
	return {
	'page_obj':context['page_obj'],
	}

@register.inclusion_tag("partials/_status_tag.html")
def status_tag(status):
	print('******',status)
	return {'status':status}



@register.simple_tag(takes_context=True)
def active_page(context,page_num):
	if context['page_obj'].number == page_num:
		return 'disabled '

@register.tag()
def create_page_link(parser, token):
	try:
		# split_contents() knows not to split quoted strings.
		tag_name, format_string = token.split_contents()
		print(format_string)
	except ValueError:
		raise template.TemplateSyntaxError(
			"%r tag requires a single argument" % token.contents.split()[0]
		)
	if not (format_string[0] == format_string[-1] and format_string[0] in ('"', "'")):
		raise template.TemplateSyntaxError(
			"%r tag's argument should be in quotes" % tag_name
		)
	return CurrentLinkNode(format_string[1:-1])

class CurrentLinkNode(template.Node):
	def __init__(self, format_string):
		self.format_string = format_string

	def render(self, context):
		page_obj=context['page_obj']
		number=page_obj.number

		num_pages=page_obj.paginator.num_pages
		result=[]
		if num_pages-2 <=3:
			for page_num in range(2,num_pages):
				active=''
				if page_num == number:
					active='disabled'
				result.append(
					f'<li class="page-item"><a class="page-link {active}" href="#">{page_num}</a></li>'
					)
		else:
			if number <=2:
				for page_num in range(2,4):
					active=''
					if page_num == number:
						active='disabled'
					result.append(
						f'<li class="page-item"><a class="page-link {active}" href="#">{page_num}</a></li>'
						)
				result.append(
						f'<li class="page-item"><a class="page-link disabled" href="#">...</a></li>'
						)
			elif number <=4:
				for page_num in range(2,number+2):
					active=''
					if page_num == number:
						active='disabled'
					result.append(
							f'<li class="page-item"><a class="page-link {active}" href="#">{page_num}</a></li>'
							)
				result.append(
						f'<li class="page-item"><a class="page-link disabled" href="#">...</a></li>'
						)					
			elif number >= num_pages-2:
				result.append(
						f'<li class="page-item"><a class="page-link disabled" href="#">...</a></li>'
						)
				for page_num in range(num_pages-2,num_pages):
					active=''

					if page_num == number:
						active='disabled'
					result.append(
						f'<li class="page-item"><a class="page-link {active}" href="#">{page_num}</a></li>'
						)

			else:
				result.append(
						f'<li class="page-item"><a class="page-link disabled" href="#">...</a></li>'
						)
				for page_num in range(number-1,number+2):
					active=''
					if page_num == number:
						active='disabled'
					result.append(
						f'<li class="page-item"><a class="page-link {active}" href="#">{page_num}</a></li>'
						)
				result.append(
						f'<li class="page-item"><a class="page-link disabled" href="#">...</a></li>'
						)
		

		return ''.join(result)
