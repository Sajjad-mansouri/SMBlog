from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

class CustomCreationForm(UserCreationForm):
	class Meta(UserCreationForm.Meta):
		model=get_user_model()
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields['password1'].help_text=None