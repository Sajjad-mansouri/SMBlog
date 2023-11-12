from django.urls import path
from .views import PostList,PostDetail,CategoryList,CategoryPostList

urlpatterns = [
	path("posts/", PostList.as_view()),
	path("posts/<int:pk>", PostDetail.as_view()),

	path("categories/", CategoryList.as_view()),
	path("categories/<int:pk>", CategoryPostList.as_view()),
]