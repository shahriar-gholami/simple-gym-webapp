
from django import forms

class CustomerRegisterForm(forms.Form):

	name = forms.CharField()
	family_name = forms.CharField()
	phone_number = forms.CharField()
	birthday = forms.CharField()
	national_code = forms.CharField()
	ensurance = forms.CharField()

class CourseRegisterForm(forms.Form):
	title = forms.CharField()
	customer = forms.CharField()
	reserved_sessions = forms.IntegerField()
	cost_paid = forms.IntegerField()
	instructor = forms.CharField()

class SelectInstructor(forms.Form):
	instructor = forms.CharField()