from rest_framework import generics
from .serializers import PostSerializer,CategorySerializer
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from blog.models import Post,Category
from .permissions import IsAuthorOrReadonly,IsSuperUser


class PostList(generics.ListCreateAPIView):
	queryset = Post.objects.all()
	serializer_class = PostSerializer
	permission_classes=[IsAuthorOrReadonly|IsSuperUser]

	@method_decorator(cache_page(300))
	def get(self, request, *args, **kwargs):
		return super().get(request,*args,**kwargs)


class PostDetail(generics.RetrieveUpdateDestroyAPIView):
	queryset = Post.objects.all()
	serializer_class = PostSerializer
	permission_classes=[IsAuthorOrReadonly|IsSuperUser]

	@method_decorator(cache_page(300))
	def get(self, request, *args, **kwargs):
		return super().get(request,*args,**kwargs)


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