from rest_framework import generics
from .serializers import PostSerializer,CategorySerializer
from blog.models import Post,Category


class PostList(generics.ListCreateAPIView):
	queryset = Post.objects.all()
	serializer_class = PostSerializer


class PostDetail(generics.RetrieveUpdateDestroyAPIView):
	queryset = Post.objects.all()
	serializer_class = PostSerializer

class CategoryList(generics.ListCreateAPIView):
	queryset = Category.objects.all()
	serializer_class = CategorySerializer


class CategoryPostList(generics.ListAPIView):
	serializer_class = PostSerializer

	def get_queryset(self):

		pk=self.kwargs['pk']
		category=Category.objects.get(id=pk)
		return category.articles.all()