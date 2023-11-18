from .forms import  UserProfileForm,AuthorPostForm,SuperUserPostForm
class AuthorMixin:
	def get_form(self,form_class=None):
	
		if self.request.user.is_superuser:
			form_class=SuperUserPostForm	
		else:
			form_class=AuthorPostForm	
		return form_class(**self.get_form_kwargs())



	def form_valid(self,form):
		self.object=form.save(commit=False)
		self.object.author=self.request.user
		return super().form_valid(form=self.object)
