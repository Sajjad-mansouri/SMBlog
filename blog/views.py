from django.shortcuts import render
from django.views.generic import ListView,DetailView,FormView,TemplateView
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.db.models import Q
from django.contrib.auth import get_user_model
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.messages.views import SuccessMessageMixin
from django.http import JsonResponse
from django.contrib import messages
from .models import Post,Category,AboutCategory
from .forms import  ContactMeForm
from account.tasks import send_email

class Index(ListView):
	template_name='blog/index.html'
	context_object_name='posts'
	paginate_by=3


	def get_queryset(self):
		return Post.objects.prefetch_related('category').select_related('author').filter(status='p')


class PostDetailView(DetailView):
	template_name='blog/post_detail.html'
	queryset=Post.objects.prefetch_related('hits').filter(status='p')

	def get_object(self):
		slug=self.kwargs.get('slug')
		post=get_object_or_404(self.queryset,slug=slug)
		ip_address=self.request.ip_address
		if not ip_address in post.hits.all():
			post.hits.add(ip_address)
		return post


class CategoryPostList(ListView):
	template_name='blog/index.html'
	context_object_name='posts'
	paginate_by=3

	def get_queryset(self):
		cat_slug=self.kwargs.get('cat')
		self.category=Category.objects.get(slug=cat_slug)
		return self.category.articles.prefetch_related('category').select_related('author').filter(status='p')
	def get_context_data(self,**kwargs):
		kwargs=super().get_context_data(**kwargs)
		kwargs['category']=self.category
		return kwargs

class Search(ListView):
	template_name='blog/index.html'
	context_object_name='posts'

	def get_queryset(self):
		self.search_var=self.request.GET.get('search')
		try:
			post=Post.objects.prefetch_related('category').filter(
				(Q(title__icontains=self.search_var)|
				Q(description__icontains=self.search_var)|
				Q(author__first_name__icontains=self.search_var)
				)&
				Q(status='p')
				)
		except ValueError:
			post=Post.objects.filter(status='p')


		return post
	def get_context_data(self,**kwargs):
		kwargs=super().get_context_data(**kwargs)
		kwargs['search']=self.search_var
		return kwargs


class ContactMe(SuccessMessageMixin,FormView):
	template_name='blog/contact_me.html'
	form_class=ContactMeForm
	success_url=reverse_lazy('blog:contact_me')
	try:
		owner=get_user_model().objects.get(is_superuser=True)
	except Exception as e:
		print(e)
	def get_context_data(self,**kwargs):
		context=super().get_context_data(**kwargs)
		context['owner']= self.owner
		return context

	def form_valid(self,form):
		current_site = get_current_site(self.request).name
		name=form.cleaned_data['name']
		email=form.cleaned_data['email']
		subject=form.cleaned_data['subject']
		message=form.cleaned_data['message']
		context={
			'name':name,
			'current_site':current_site,
			'owner':self.owner.get_full_name(),
			'message':message,
			'email':email
		}
		email_template_name='blog/contact_email.html'
		subject_template_name='blog/contact_subject.txt'
		admin_email_template='blog/admin_email_template.html'
		#send email to person who message
		send_email.delay(
			subject_template_name,
			email_template_name,		
			context,
			from_email=None,
			to_email=email
			)

		#send to admin
		send_email.delay(
			subject,
			admin_email_template,
			context,
			from_email=None,
			to_email=self.owner.email

			)
		messages=f'Dear {name}, Thank you for your valuable feedback.'
		return JsonResponse({'message':messages})

class About(ListView):
	template_name='blog/about.html'
	queryset=AboutCategory.objects.prefetch_related('about_set')