from rest_framework import generics,viewsets
from .serializers import PostSerializer,CategorySerializer
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_headers
from blog.models import Post,Category
from .permissions import IsAuthorOrReadonly,IsSuperUser


class PostApiViewSet(viewsets.ModelViewSet):
	queryset = Post.objects.all()
	serializer_class = PostSerializer

	@method_decorator(cache_page(300))
	@method_decorator(vary_on_headers("Authorization",'Cookie'))
	def list(self, request, *args, **kwargs):
		return super().list(request,*args,**kwargs)


class CategoryList(generics.ListCreateAPIView):
	queryset = Category.objects.all()
	serializer_class = CategorySerializer
	permission_classes=[IsSuperUser]


class CategoryPostList(generics.ListAPIView):
	serializer_class = PostSerializer

	def get_queryset(self):

		pk=self.kwargs['pk']
		category=Category.objects.get(id=pk)
		return category.articles.all()