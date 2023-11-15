from django.shortcuts import render
from django.views.generic import CreateView
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy

#for registration
from .send_confirmation import EmailConfirmation
from .forms import CustomCreationForm

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
		return super().form_valid(form)

