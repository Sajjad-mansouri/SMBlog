from django.shortcuts import render
from django.views.generic import ListView,DetailView
from django.shortcuts import get_object_or_404
from django.db.models import Q
from .models import Post,Category


class Index(ListView):
	template_name='blog/index.html'
	context_object_name='posts'
	paginate_by=3


	def get_queryset(self):
		return Post.objects.filter(status='p')


class PostDetailView(DetailView):
	template_name='blog/post_detail.html'
	queryset=Post.objects.filter(status='p')

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

	def get_queryset(self):
		cat_slug=self.kwargs.get('cat')
		self.category=Category.objects.get(slug=cat_slug)
		return self.category.articles.filter(status='p')
	def get_context_data(self,**kwargs):
		kwargs=super().get_context_data(**kwargs)
		kwargs['category']=self.category
		return kwargs

class Search(ListView):
	template_name='blog/index.html'
	context_object_name='posts'

	def get_queryset(self):
		print('queryset')
		self.search_var=self.request.GET.get('search')
		try:
			post=Post.objects.filter(
				(Q(title__icontains=self.search_var)|
				Q(description__icontains=self.search_var)|
				Q(author__first_name__icontains=self.search_var)
				)&
				Q(status='p')
				)
			print(post)
		except ValueError:
			post=Post.objects.filter(status='p')


		return post
	def get_context_data(self,**kwargs):
		kwargs=super().get_context_data(**kwargs)
		kwargs['search']=self.search_var
		return kwargs
