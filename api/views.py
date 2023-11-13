from rest_framework import generics
from .serializers import PostSerializer,CategorySerializer
from blog.models import Post,Category
from .permissions import IsAuthorOrReadonly,IsSuperUser


class PostList(generics.ListCreateAPIView):
	queryset = Post.objects.all()
	serializer_class = PostSerializer
	permission_classes=[IsAuthorOrReadonly|IsSuperUser]


class PostDetail(generics.RetrieveUpdateDestroyAPIView):
	queryset = Post.objects.all()
	serializer_class = PostSerializer
	permission_classes=[IsAuthorOrReadonly|IsSuperUser]

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