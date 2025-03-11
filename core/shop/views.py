from django.shortcuts import render, redirect
from .forms import *
from django.views import View
from shop.models import *

class CustomerRegister(View):

	template_name = f'shop/customer_register.html'
	def get(self, request):
		form = CustomerRegisterForm
		customers = Customer.objects.all()
		return render(request, self.template_name, {'form': form, 'customers':customers})
	
	def post(self, request):
		form = CustomerRegisterForm(request.POST)
		if form.is_valid():
			name = form.cleaned_data['name']
			family_name = form.cleaned_data['family_name']
			full_name = name + " " + family_name
			phone_number = form.cleaned_data['phone_number']
			birthday = form.cleaned_data['birthday']
			birth_day = birthday[:-10]
			national_code = form.cleaned_data['national_code']
			ensurance = form.cleaned_data['ensurance']
			if ensurance == '0':
				ensure_status = False
			else:
				ensure_status = True
			if Customer.objects.filter(national_code = national_code).first() == None:
				new_customer = Customer.objects.create(
					full_name = full_name,
					phone_number = phone_number,
					birthday = birth_day,
					national_code = national_code, 
					ensurance = ensure_status
				)
				return redirect(f'shop:index')
			else:
				customers = Customer.objects.all()
				return render(request, self.template_name, {'form': form, 'message':'کاربر با این کد ملی قبلا در سامانه ثبت نام شده است.', 'customers':customers})
		customers = Customer.objects.all()
		return render(request, self.template_name, {'form': form, 'message':'اطلاعات به صورت ناقص وارد شده است.', 'customers':customers})
	
class CourseRegisterView(View):

	template_name = f'shop/course_register.html'

	def get(self, request):
		customers = Customer.objects.all()
		courses = CourseTitle.objects.all()
		form = CourseRegisterForm()
		return render(request, self.template_name, {'form': form, 'customers':customers, 'courses':courses})

	def post(self, request):
		customers = Customer.objects.all()
		courses = CourseTitle.objects.all()
		form = CourseRegisterForm(request.POST)
		if form.is_valid():
			customer_id = form.cleaned_data['customer']
			customer = Customer.objects.get(id = customer_id)
			title_id = form.cleaned_data['title']
			course_title = CourseTitle.objects.get(id = title_id)
			register_date = form.cleaned_data['register_date']
			reserved_sessions = form.cleaned_data['reserved_sessions']
			cost_paid = form.cleaned_data['cost_paid']
			new_reserve = ReservedCourse.objects.create(
				customer = customer,
				title = course_title,
				num_of_sessions = reserved_sessions,
				cost_paid = cost_paid,
				register_date = register_date
			)
			success_message = 'ثبت نام مشترک با موفقیت انجام شد.' 
			return render(request, self.template_name, {'form': form, 'customers':customers, 'courses':courses, 'success_message':success_message})
		fail_message = 'ثبت نام مشترک با موفقیت انجام نشد. اطلاعات ورودی ناقص یا نامعتبر.' 
		return render(request, self.template_name, {'form': form, 'customers':customers, 'courses':courses, 'fail_message':fail_message})

class DeleteCustomerView(View):

	def get(self, request, customer_id):
		customer = Customer.objects.get(id = customer_id)
		customer.delete()
		return redirect('shop:index')