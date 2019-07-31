from django.http import HttpResponse
from django.shortcuts import render
from .forms import ContactForm

def home_page(request):
	return render(request, "home.html", {"title" : "HOME"})

def contact_page(request):
	form = ContactForm(request.POST or None)
	if form.is_valid():
		print(form.cleaned_data)
		form  = ContactForm()	
	else:
		print(form.errors)
	context = {"title" : 'Contact Us', "form" : form}
	return render(request, "forms.html", context)