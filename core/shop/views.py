from django.shortcuts import render, redirect
from .forms import *
from django.views import View
from django.utils.timezone import now  # وارد کردن now از django.utils.timezone
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
		form = CourseRegisterForm
		instructors = Instructor.objects.all()
		return render(request, self.template_name, {'form': form, 
													'customers':customers, 
													'courses':courses, 
													'instructors':instructors})

	def post(self, request):
		customers = Customer.objects.all()
		courses = CourseTitle.objects.all()
		form = CourseRegisterForm(request.POST)
		if form.is_valid():
			customer_id = form.cleaned_data['customer']
			customer = Customer.objects.get(id = customer_id)
			title_id = form.cleaned_data['title']
			course_title = CourseTitle.objects.get(id = title_id)
			reserved_sessions = form.cleaned_data['reserved_sessions']
			cost_paid = form.cleaned_data['cost_paid']
			instructor_id = form.cleaned_data['instructor']
			date = form.cleaned_data['date'].replace('سه شنبه', 'سه‌شنبه').replace('چهار شنبه', 'چهارشنبه')
			instructor = Instructor.objects.get(id=instructor_id)

			new_reserve = ReservedCourse.objects.create(
				customer = customer,
				title = course_title,
				num_of_sessions = reserved_sessions,
				cost_paid = cost_paid,
				instructor = instructor,
				register_date = date
			)
			
			instructor_monthly_income = InstructorMonthlyIncome.objects.filter(month=new_reserve.shamsi_register_month,year=new_reserve.shamsi_register_year,instructor=instructor).first()
			if instructor_monthly_income != None:
				instructor_monthly_income.courses.add(new_reserve)
			else:
				new_instructor_monthly_income = InstructorMonthlyIncome.objects.create(
					instructor = instructor,
					month = new_reserve.shamsi_register_month,
					year = new_reserve.shamsi_register_year,
				)
				new_instructor_monthly_income.courses.add(new_reserve)
				new_instructor_monthly_income.save()
			success_message = 'ثبت نام مشترک با موفقیت انجام شد.' 
			return render(request, self.template_name, {'form': form, 'customers':customers, 'courses':courses, 'success_message':success_message})
		fail_message = 'ثبت نام مشترک با موفقیت انجام نشد. اطلاعات ورودی ناقص یا نامعتبر.' 
		return render(request, self.template_name, {'form': form, 'customers':customers, 'courses':courses, 'fail_message':fail_message})

class DeleteCustomerView(View):

	def get(self, request, customer_id):
		customer = Customer.objects.get(id = customer_id)
		customer.delete()
		return redirect('shop:index')
	
class InstructorFinanceView(View):

	template_name = 'shop/instructor_finance.html'

	def get(self, request, instructor_id):
		form = SelectInstructor
		instructors = Instructor.objects.all()
		if instructor_id != 0:
			instructor = Instructor.objects.get(id = instructor_id)
			instructor_monthly_income = InstructorMonthlyIncome.objects.filter(instructor=instructor)
			years = list(set([income.year for income in instructor_monthly_income]))
			monthes = list(set([income.month for income in instructor_monthly_income]))
			return render(request, self.template_name, {'form':form, 
											   			'instructor_monthly_income':instructor_monthly_income,
														'instructors':instructors,
														'monthes':monthes,
														'years':years})
		else:
			return render(request, self.template_name, {'form':form, 
														'instructors':instructors})

	def post(self, request, instructor_id):
		form = SelectInstructor(request.POST)
		if form.is_valid():
			instructor_id = form.cleaned_data['instructor']
			instructor = Instructor.objects.get(id = instructor_id)
			return redirect('shop:instructor_finance', instructor_id)

class SubmitPaymentsView(View):
	 
	template_name = 'shop/submit_payments.html'

	def get(self, request):
		form = InstructorDeptForm
		instructors = Instructor.objects.all()
		instructor_monthly_incomes = InstructorMonthlyIncome.objects.filter(is_paid=False)
		payments = PaymentRecord.objects.all()
		years = list(set([payment.shamsi_created_year for payment in payments]))
		monthes = list(set([payment.shamsi_created_month for payment in payments]))
		return render(request, self.template_name, {'form':form, 
											   			# 'instructor_monthly_income':instructor_monthly_income,
														'instructors':instructors,
														'payments':payments,
														'instructor_monthly_incomes':instructor_monthly_incomes,
														'monthes':monthes,
														'years':years
														})
	
class ConfirmInstructorPaymentView(View):

	def post(self, request):
		
		form = InstructorDeptForm(request.POST)
		if form.is_valid():
			instructor_dept_id = form.cleaned_data['instructore_income']
			instructor_dept = InstructorMonthlyIncome.objects.get(id = int(instructor_dept_id))
			instructor_dept.is_paid = True
			instructor_dept.pay_date = now()
			instructor_dept.save()
			new_payment_record = PaymentRecord.objects.create(
				amount = instructor_dept.get_self_share(),
				description = f'پرداختی مربی {instructor_dept.instructor.full_name} برای دوره {instructor_dept.shamsi_pay_year}/{instructor_dept.shamsi_pay_month}',
			)
			return redirect('shop:payments')
		
class SubmitGymCostsView(View):

	def post(self, request):
		
		form = GymCosts(request.POST)
		if form.is_valid():
			description = form.cleaned_data['description']
			amount = int(form.cleaned_data['amount'])
			new_payment_record = PaymentRecord.objects.create(
				amount = amount,
				description = description,
			)
			return redirect('shop:payments')

class InstructorsView(View):

	template_name = 'shop/instructors.html'

	def get(self, request):
		instructors = Instructor.objects.all()
		form = InstructorRegister
		courses = CourseTitle.objects.all()
		return render(request, self.template_name, {
			'form':form,
			'instructors':instructors,
			'courses':courses,
		})
	
	def post(self, request):
		form = InstructorRegister(request.POST)
		courses = request.POST.getlist('courses')

		if form.is_valid():
			full_name = form.cleaned_data['full_name']
			phone_number = form.cleaned_data['phone_number']
			national_code = form.cleaned_data['national_code']
			share_percent = form.cleaned_data['share_percent']
			birthday = form.cleaned_data['birthday']
			study = form.cleaned_data['study']
			address = form.cleaned_data['address']
			# ایجاد مربی جدید
			new_instructor = Instructor.objects.create(
				full_name=full_name,
				phone_number=phone_number,
				national_code=national_code,
				share_percent=share_percent,
				birthday = birthday,
				study = study, 
				address = address
			)
			
			# اضافه کردن دوره‌ها به مربی
			for course_id in courses:
				if course_id != '0':  # اگر "همه دوره‌ها" انتخاب نشده باشد
					course = CourseTitle.objects.get(id=int(course_id))
					new_instructor.courses.add(course)
				else:
					course = CourseTitle.objects.all()
					new_instructor.courses.add(*course)
			
			return redirect('shop:instructors')  # تغییر مسیر پس از ثبت موفق
		else:
			# اگر فرم معتبر نباشد، فرم را دوباره نمایش دهید
			courses = CourseTitle.objects.all()
			return render(request, self.template_name, {'form': form, 'courses': courses, 'fail_message':'ثبت‌نام مربی انجام نشد. اطلاعات ورودی نامعتبر یا ناقص'})

class DeleteInstructorView(View):

	def get(self, request, instructor_id):
		instructor = Instructor.objects.get(id = instructor_id)
		instructor.delete()
		return redirect('shop:instructors')
	
class CoursesView(View):

	template_name = 'shop/courses.html'

	def get(self, request):

		courses = CourseTitle.objects.all()
		form = CourseAdd
		return render(request, self.template_name, {'courses':courses, 'form':form})
	
	def post(self, request):

		form = CourseAdd(request.POST)
		if form.is_valid():
			title = form.cleaned_data['title']
			new_course = CourseTitle.objects.create(
				title = title
			)
			return redirect('shop:courses')
		
class DeleteCourseView(View):

	def get(self, request, course_id):
		course = CourseTitle.objects.get(id = course_id)
		course.delete()
		return redirect('shop:courses')















