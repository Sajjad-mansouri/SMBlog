from django.http import HttpResponseRedirect
from .forms import  UserProfileForm,AuthorPostForm,SuperUserPostForm
from blog.models import Post

class AuthorQuerySet:
	def get_queryset(self):
		print(dir(self))
		user=self.request.user
		if user.is_superuser:
			posts=Post.objects.all()
		else:
			posts=Post.objects.filter(author=user)
		return posts



class AuthorMixin(AuthorQuerySet):
	def get_form(self,form_class=None):
	
		if self.request.user.is_superuser:
			form_class=SuperUserPostForm	
		else:
			form_class=AuthorPostForm	
		return form_class(**self.get_form_kwargs())



	def form_valid(self,form):
		self.object=form.save(commit=False)
		if not self.request.user.is_superuser:
			self.object.author=self.request.user
		if not self.request.user.is_superuser and self.object.status not in ('d','s'):
			self.object.status='d'
		self.object.save()
		form.save_m2m()
		return HttpResponseRedirect(self.get_success_url())

