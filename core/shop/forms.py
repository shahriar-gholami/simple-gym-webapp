
from django import forms

class CustomerRegisterForm(forms.Form):

	full_name = forms.CharField()
	phone_number = forms.CharField()


class CourseRegisterForm(forms.Form):
	title = forms.CharField()
	customer = forms.CharField()
	register_date = forms.CharField()
	reserved_sessions = forms.IntegerField()
	cost_paid = forms.IntegerField()