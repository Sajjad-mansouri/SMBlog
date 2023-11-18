from django.urls import path,include
from . import views
from . import confirmation

urlpatterns=[
    path('profile/<int:pk>/',views.Profile.as_view(),name='profile'),
    path('profile/create-post/',views.CreatePost.as_view(),name='create-post'),
    path('profile/<int:pk>/posts/',views.AuthorPostList.as_view(),name='author-posts'),
    path('profile/posts/<int:pk>/',views.UpdatePost.as_view(),name='update-post'),


	path('register/',views.Register.as_view(),name='register'),
    path(
        "confirm/<uidb64>/<token>/",
        confirmation.EmailConfirmView.as_view(),
        name="email_confirm",
    ),
	path('',include('django.contrib.auth.urls'))
]