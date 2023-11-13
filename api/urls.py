from django.urls import path,include
from .views import PostApiViewSet,CategoryList,CategoryPostList
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'posts', PostApiViewSet, basename='posts')

urlpatterns = [

	path("categories/", CategoryList.as_view(),name='api_category_list'),
	path("categories/<int:pk>", CategoryPostList.as_view(),name='api_category_post_list'),

	path("auth/", include("rest_framework.urls")),

	#JWT
	path("jwt/", TokenObtainPairView.as_view(),name="jwt_obtain_pair"),
	path("jwt/refresh/", TokenRefreshView.as_view(),name="jwt_refresh"),
]

urlpatterns+=router.urls