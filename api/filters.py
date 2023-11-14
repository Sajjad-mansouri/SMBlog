from django_filters import rest_framework as filters
from blog.models import Post

class PostFilterSet(filters.FilterSet):
	published_from=filters.DateFilter(
			field_name='published',
			lookup_expr='lte',
			label='Published Date To'
		)
	published_to=filters.DateFilter(
			field_name='published',
			lookup_expr='gte',
			label='Published Date From'
		)

	description=filters.CharFilter(
			field_name='description',
			lookup_expr='icontains',
			label='Content contain'
		)

	class Meta:
		model=Post
		fields=['author','category']