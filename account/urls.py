from django.urls import path,include
from . import views
from . import confirmation

extra_patterns=[
    path('<int:pk>/',views.Profile.as_view(),name='profile'),
    path('create-post/',views.CreatePost.as_view(),name='create-post'),
    path('posts/<int:pk>/',views.AuthorPostList.as_view(),name='author-posts'),
    path('posts/<int:pk>/',views.UpdatePost.as_view(),name='update-post'),
    path('posts/<int:pk>/',views.UpdatePost.as_view(),name='update-post'),
    path('posts/<int:pk>/delete',views.DeletePost.as_view(),name='delete-post'),
    path('posts/preview/<int:pk>/',views.PostPreview.as_view(),name='post-preview'),
]
urlpatterns=[

    path("profile/", include(extra_patterns)),
	path('register/',views.Register.as_view(),name='register'),
    path(
        "confirm/<uidb64>/<token>/",
        confirmation.EmailConfirmView.as_view(),
        name="email_confirm",
    ),
	path('',include('django.contrib.auth.urls'))
]