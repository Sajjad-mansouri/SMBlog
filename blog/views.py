from django.shortcuts import render
from django.views.generic import ListView
from .models import Post,Category


class Index(ListView):
	template_name='blog/index.html'
	context_object_name='posts'


	def get_queryset(self):
		return Post.objects.filter(status='p')

