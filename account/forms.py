from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth import get_user_model
from blog.models import Post

class CustomCreationForm(UserCreationForm):
	email=forms.EmailField()
	class Meta(UserCreationForm.Meta):
		model=get_user_model()
		fields=('username','email',)
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields['password1'].help_text=None


class UserProfileForm(forms.ModelForm):
	def __init__(self,*args,**kwargs):
		super().__init__(*args,**kwargs)
		self.fields['is_author'].disabled=True
	class Meta:
		model=get_user_model()
		fields=['first_name','last_name','username','email','is_author','profile_image']

class SuperUserPostForm(forms.ModelForm):

	class Meta:
		model=Post
		fields='__all__'

class AuthorPostForm(SuperUserPostForm):
	def __init__(self,*args,**kwargs):
		super().__init__(*args,**kwargs)
		self.fields['status'].choices=[('d','Draft'),('s','Send to Manager')]

	class Meta(SuperUserPostForm.Meta):
		exclude=['author']


