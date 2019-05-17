from django import forms
from django.forms import ModelForm, Textarea, IntegerField
from . import models

class OsobaForm(forms.Form):
	imie = forms.CharField(label = "imie")
	nazwisko = forms.CharField(label = "nazwisko")

class TelefonForm(forms.Form):
	telefon = forms.IntegerField(label = "telefon")

class EmailForm(forms.Form):
	email = forms.EmailField(label = "email")



	

