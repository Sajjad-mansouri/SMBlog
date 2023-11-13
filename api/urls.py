from django.urls import path,include
from .views import PostList,PostDetail,CategoryList,CategoryPostList
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
	path("posts/", PostList.as_view(),name='api_post_list'),
	path("posts/<int:pk>", PostDetail.as_view(),name='api_post_detail'),

	path("categories/", CategoryList.as_view(),name='api_category_list'),
	path("categories/<int:pk>", CategoryPostList.as_view(),name='api_category_post_list'),

	path("auth/", include("rest_framework.urls")),

	#JWT
	path("jwt/", TokenObtainPairView.as_view(),name="jwt_obtain_pair"),
	path("jwt/refresh/", TokenRefreshView.as_view(),name="jwt_refresh"),
]