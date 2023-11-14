from django.urls import path
from . import views


app_name='blog'
urlpatterns=[
	path('',views.Index.as_view(),name='index'),
	path('post/<int:pk>/',views.PostDetailView.as_view(),name='post_detail'),
	path('category/<slug:cat>/',views.CategoryPostList.as_view(),name='category_post_list'),

]