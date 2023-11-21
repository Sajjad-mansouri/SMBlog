from django.shortcuts import render
from django.views.generic import CreateView,ListView,UpdateView,DeleteView,DetailView
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy,reverse
from django.http import HttpResponseRedirect
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import  UserProfileForm,AuthorPostForm,SuperUserPostForm
from blog.models import Post
from .forms import CustomCreationForm
from .mixins import AuthorMixin,AuthorQuerySet
#for registration
from .confirmation import EmailConfirmation


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


class Profile(LoginRequiredMixin,UpdateView):
	model=User_Model
	template_name='profile/profile.html'
	form_class=UserProfileForm

	def get_success_url(self):
		return reverse('profile',args=(self.request.user.pk,))


class CreatePost(LoginRequiredMixin,AuthorMixin,CreateView):

	template_name='profile/create_update_post.html'

	def get_success_url(self):
		return reverse('author-posts',args=(self.request.user.pk,))

class UpdatePost(LoginRequiredMixin,AuthorMixin,UpdateView):
	template_name='profile/create_update_post.html'
	

	def get_success_url(self):
		return reverse('author-posts',args=(self.request.user.pk,))
	def get_queryset(self):
		user=self.request.user
		if user.is_superuser:
			queryset=Post.objects.all()
		else:
			queryset=Post.objects.filter(author=user,status__in=['d','r'])
		return queryset

class AuthorPostList(LoginRequiredMixin,AuthorMixin,ListView):
	template_name='profile/post_list.html'
	paginate_by=5




class DeletePost(LoginRequiredMixin,DeleteView):
	template_name='profile/confirm_delete.html'
	def get_success_url(self):
		return reverse('author-posts',args=(self.request.user.pk,))

	def get_queryset(self):
		user=self.request.user
		if user.is_superuser:
			queryset=Post.objects.all()
		else:
			queryset=Post.objects.filter(author=user,status='d')
		return queryset

class PostPreview(LoginRequiredMixin,DetailView):
	template_name='blog/post_detail.html'
	extra_context={'preview':'preview'}
	def get_queryset(self):
		user=self.request.user
		if user.is_superuser:
			queryset= Post.objects.exclude(status = 'p')
		else:
			queryset=Post.objects.filter(Q(author=user)& Q(status__in='drs'))
		return queryset


