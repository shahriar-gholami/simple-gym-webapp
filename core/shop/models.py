from django.db import models
from django.utils.translation import gettext_lazy as _
from khayyam import JalaliDatetime
from django.utils.timezone import now
from django.db.models import Sum




class CourseTitle(models.Model):
	title = models.CharField(max_length=250)

	def __str__(self):
		return f'{self.title}'

class Customer(models.Model):
	full_name = models.CharField(max_length=30)
	create_date = models.DateTimeField(default=now)  # مقدار پیش‌فرض به‌جای auto_now_add
	birthday = models.CharField(max_length=250, null=True, blank=True)
	ensurance = models.BooleanField(default=False)
	national_code = models.CharField(max_length=250, unique=True, null=True, blank=True)
	phone_number = models.CharField(max_length=250)

	def get_courses(self):
		return ReservedCourse.objects.filter(customer=self)
	
	def get_total_payments(self):
		total = 0
		courses = ReservedCourse.objects.filter(customer=self)
		if courses == None:
			return total
		else:
			for course in courses:
				total = total + course.cost_paid
			return total

	@property
	def register_date(self):
		return JalaliDatetime(self.create_date).strftime('%Y/%m/%d')
	
	def __str__(self):
		return f'{self.full_name}'

class Instructor(models.Model):
	full_name = models.CharField(max_length=250)
	phone_number = models.CharField(max_length=250)
	national_code = models.CharField(max_length=250)
	courses = models.ManyToManyField(CourseTitle, blank=True)
	created_date = models.DateTimeField(auto_now_add=True, null=True)
	share_percent = models.IntegerField(default=70)
	birthday = models.CharField(max_length=250, null=True, blank=True)
	study = models.CharField(max_length=250, null=True, blank=True)
	address = models.TextField(null=True, blank=True)

	@property
	def register_date(self):
		return JalaliDatetime(self.created_date).strftime('%Y/%m/%d')

	def get_monthly_income(self, year, month):
		"""
		مجموع هزینه دوره‌های مربی برای یک ماه شمسی خاص
		:param year: سال شمسی (مثلاً 1402)
		:param month: ماه شمسی (مثلاً 1 برای فروردین)
		:return: مجموع هزینه‌ها
		"""
		# فیلتر دوره‌های مربوط به مربی و ماه شمسی مورد نظر
		monthly_courses = ReservedCourse.objects.filter(
			instructor=self,
			register_date__year=year,
			register_date__month=month
		)
		# محاسبه مجموع هزینه‌ها
		total_income = monthly_courses.aggregate(total_income=Sum('cost_paid'))['total_income']
		return total_income or 0  # اگر هیچ دوره‌ای نبود، 0 برگردان
	
	def __str__(self):
		return self.full_name

class InstructorMonthlyIncome(models.Model):
	instructor = models.ForeignKey(Instructor, on_delete=models.CASCADE)
	month = models.IntegerField(default=1)
	year = models.IntegerField(default=1403)
	courses =models.ManyToManyField('ReservedCourse', blank=True)
	is_paid = models.BooleanField(default=False)
	pay_date = models.DateTimeField(default=now, null=True, blank=True)

	def get_monthly_income(self):
		income = 0
		for course in self.courses.all():
			income = income + course.cost_paid
		return income
	
	def get_self_share(self):
		share = self.instructor.share_percent
		return self.get_monthly_income()*share/100
	
	def get_gym_share(self):
		return self.get_monthly_income() - self.get_self_share()
	
	@property
	def shamsi_pay_date(self):
		return JalaliDatetime(self.pay_date).strftime('%Y/%m/%d')	

	@property
	def shamsi_pay_year(self):
		return int(JalaliDatetime(self.pay_date).strftime('%Y'))

	@property
	def shamsi_pay_month(self):
		return int(JalaliDatetime(self.pay_date).strftime('%m'))	
	
	def __str__(self):
		return f'{self.instructor.full_name} - {self.year}/{self.month}'

class ReservedCourse(models.Model):
	title = models.ForeignKey(CourseTitle, on_delete=models.CASCADE)
	customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
	num_of_sessions = models.IntegerField(default=0)
	cost_paid = models.IntegerField(default=0)
	register_date = models.CharField(max_length=250, null=True, blank=True)
	instructor = models.ForeignKey(Instructor, on_delete=models.CASCADE, null=True, blank=True)

	@property
	def shamsi_register_year(self):
		year = self.register_date.split()[3]
		if year == '۱۴۰۰':
			year_num = 1400
		elif year == '۱۴۰۱':
			year_num = 1401
		elif year == '۱۴۰۲':
			year_num = 1402
		elif year == '۱۴۰۳':
			year_num = 1403
		elif year == '۱۴۰۴':
			year_num = 1404
		elif year == '۱۴۰۵':
			year_num = 1405
		elif year == '۱۴۰۶':
			year_num = 1405
		return year_num

	@property
	def shamsi_register_month(self):
		month = self.register_date.split()[2]
		if month == 'فروردین':
			month_num = 1
		elif month == 'اردیبهشت':
			month_num = 2
		elif month == 'خرداد':
			month_num = 3
		elif month == 'تیر':
			month_num = 4
		elif month == 'مرداد':
			month_num = 5
		elif month == 'شهریور':
			month_num = 6
		elif month == 'مهر':
			month_num = 7
		elif month == 'آبان':
			month_num = 8
		elif month == 'آذر':
			month_num = 9
		elif month == 'دی':
			month_num = 10
		elif month == 'بهمن':
			month_num = 11
		elif month == 'اسفند':
			month_num = 12
		return month_num		

	def __str__(self):
		return f'{self.title} - {self.customer.full_name}'

class SalaryPayment(models.Model):
	amount = models.IntegerField(default=0)
	instructor = models.ForeignKey(Instructor, on_delete=models.CASCADE)
	pay_month = models.IntegerField(default=1)
	pay_year = models.IntegerField(default=1403)

	def __str__(self):
		return self.instructor.full_name

class PaymentRecord(models.Model):
	amount = models.IntegerField()
	description = models.CharField(max_length=250)
	creted_date = models.DateTimeField(auto_now_add=True)

	@property
	def shamsi_created_date(self):
		return JalaliDatetime(self.creted_date).strftime('%Y/%m/%d')	

	@property
	def shamsi_created_year(self):
		return int(JalaliDatetime(self.creted_date).strftime('%Y'))

	@property
	def shamsi_created_month(self):
		return int(JalaliDatetime(self.creted_date).strftime('%m'))
	
	def __str__(self):
		return self.description

