from django.shortcuts import render
from django.views.generic import CreateView,ListView,UpdateView
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy,reverse
from django.http import HttpResponseRedirect
from .forms import  UserProfileForm,PostForm
from blog.models import Post

#for registration
from .confirmation import EmailConfirmation
from .forms import CustomCreationForm

User_Model=get_user_model()
class Register(CreateView):
	model=get_user_model()
	form_class=CustomCreationForm
	template_name='registration/register.html'
	success_url=reverse_lazy('login')


	def form_valid(self,form):
		self.object=form.save(commit=False)
		self.object.is_active=False
		self.object.save()
		email_conf=EmailConfirmation(email=self.object.email,request=self.request)
		email_conf.save()
		return HttpResponseRedirect(self.get_success_url())


class Profile(UpdateView):
	model=User_Model
	template_name='registration/profile.html'
	form_class=UserProfileForm

	def get_success_url(self):
		return reverse('profile',args=(self.request.user.pk,))


class CreatePost(CreateView):
	model=Post
	template_name='registration/create_update_post.html'
	form_class=PostForm

	def get_success_url(self):
		return reverse('author-posts',args=(self.request.user.pk,))

class UpdatePost(UpdateView):
	template_name='registration/create_update_post.html'
	fields='__all__'
	
	def get_queryset(self):
		posts=Post.objects.filter(author=self.request.user)
		return posts

	def get_success_url(self):
		return reverse('author-posts',args=(self.request.user.pk,))

class AuthorPostList(ListView):
	template_name='registration/post_list.html'
	paginate_by=3

	def get_queryset(self):
		user=self.request.user
		posts=Post.objects.filter(author=user)
		return posts


