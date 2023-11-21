from django.urls import path
from . import views


app_name='blog'
urlpatterns=[
	path('',views.Index.as_view(),name='index'),
	path('post/<str:slug>/',views.PostDetailView.as_view(),name='post_detail'),
	path('category/<slug:cat>/',views.CategoryPostList.as_view(),name='category_post_list'),
	path('search/',views.Search.as_view(),name='search_result'),
	path('contact/',views.ContactMe.as_view(),name='contact_me'),
	path('about/',views.About.as_view(),name='about')


]