from django import forms

class ContactMeForm(forms.Form):
	name=forms.CharField()
	subject=forms.CharField()
	email=forms.EmailField()
	message=forms.CharField(widget=forms.Textarea(attrs={"rows":"3"}))