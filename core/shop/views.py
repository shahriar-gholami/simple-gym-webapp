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
			full_name = form.cleaned_data['full_name']
			phone_number = form.cleaned_data['phone_number']
			new_customer = Customer.objects.create(
				full_name = full_name,
				phone_number = phone_number
			)
			return redirect(f'shop:index')
		return render(request, self.template_name, {'form': form})
	


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

# class CouponListView(View):

# 	template_name = f'shop/owner-dashboard-coupons.html'

# 	def get(self, request):
# 		coupons = Coupon.objects.all()
# 		return render(request, self.template_name, {'coupons': coupons})
	
# 	def post(self, request):
# 		form = CouponForm(request.POST)
# 		if form.is_valid():
# 			print('WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW')
# 			print(form.cleaned_data)
# 			code = form.cleaned_data['code']
# 			from_time = form.cleaned_data['from_time']
# 			to_time = form.cleaned_data['to_time']
# 			discount = form.cleaned_data['discount']
# 			new_coupon = Coupon.objects.create(
# 											code=code,
# 											valid_from=from_time,
# 											valid_to=to_time,
# 											discount=discount)


# 			return redirect(f'shop:owner_dashboard_coupons')
# 		return render(request, self.template_name, {'form': form})

# class DeleteCouponView(View):

# 	def get(self, request, coupon_id, *args, **kwargs):
# 		coupon = Coupon.objects.get(id=coupon_id)
# 		coupon.delete()
# 		return redirect(f'shop:owner_dashboard_coupons')
