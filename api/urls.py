from django.urls import path,include
from .views import PostList,PostDetail,CategoryList,CategoryPostList
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
	path("posts/", PostList.as_view()),
	path("posts/<int:pk>", PostDetail.as_view()),

	path("categories/", CategoryList.as_view()),
	path("categories/<int:pk>", CategoryPostList.as_view()),

	path("auth/", include("rest_framework.urls")),

	#JWT
	path("jwt/", TokenObtainPairView.as_view(),name="jwt_obtain_pair"),
	path("jwt/refresh/", TokenRefreshView.as_view(),name="jwt_refresh"),
]