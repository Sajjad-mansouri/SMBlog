from django.shortcuts import render
from django.views.generic import ListView,DetailView
from .models import Post,Category


class Index(ListView):
	template_name='blog/index.html'
	context_object_name='posts'


	def get_queryset(self):
		return Post.objects.filter(status='p')


class PostDetailView(DetailView):
	template_name='blog/post_detail.html'
	queryset=Post.objects.filter(status='p')


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