from rest_framework import generics,viewsets
from .serializers import PostSerializer,CategorySerializer
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_headers
from django.db.models import Q
from datetime import timedelta
from django.utils import timezone
from django.http import Http404
from rest_framework.exceptions import ValidationError
from blog.models import Post,Category
from .permissions import IsAuthorOrReadonly,IsSuperUser
from .pagination import CustomPagination
from .filters import PostFilterSet

class PostApiViewSet(viewsets.ModelViewSet):
	queryset = Post.objects.all()
	serializer_class = PostSerializer
	pagination_class=CustomPagination
	filterset_class=PostFilterSet
	ordering_fields=['published','status','title']

	@method_decorator(cache_page(300))
	@method_decorator(vary_on_headers("Authorization",'Cookie'))
	def list(self, request, *args, **kwargs):
		return super().list(request,*args,**kwargs)

	def get_queryset(self):
		if self.request.user.is_anonymous:
			queryset= self.queryset.filter(status='p')
		elif self.request.user.is_superuser:
			queryset= self.queryset
		else:
			queryset= self.queryset.filter(Q(status='p')|Q(author=self.request.user))

		time_period_name = self.kwargs.get("period_name")

		if not time_period_name:
			return queryset

		if time_period_name == "new":
			return queryset.filter(
			published__gte=timezone.now() -timedelta(hours=1)
			)
		elif time_period_name == "today":
			return queryset.filter(
				published__date=timezone.now().date(),
			)
		elif time_period_name == "week":
			return (
				queryset.filter(published__gte=timezone.now() -timedelta(days=7))
				)
		else:
			raise Http404(f"Time period {time_period_name} is not valid,should be ")

class CategoryList(generics.ListCreateAPIView):
	queryset = Category.objects.all()
	serializer_class = CategorySerializer
	permission_classes=[IsSuperUser]
	pagination_class=None


class CategoryPostList(generics.ListAPIView):
	serializer_class = PostSerializer
	pagination_class=CustomPagination

	def get_queryset(self):

		pk=self.kwargs['pk']
		category=Category.objects.get(id=pk)
		return category.articles.all()