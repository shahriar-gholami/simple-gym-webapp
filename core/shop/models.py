from django.db import models
from django.utils.translation import gettext_lazy as _
from khayyam import JalaliDatetime
from django.utils.timezone import now



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

	@property
	def register_date(self):
		return JalaliDatetime(self.create_date).strftime('%Y/%m/%d')

class ReservedCourse(models.Model):
	title = models.ForeignKey(CourseTitle, on_delete=models.CASCADE)
	customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
	num_of_sessions = models.IntegerField(default=0)
	cost_paid = models.IntegerField(default=0)
	register_date = models.DateTimeField(auto_now_add=True)
	Instructor = models.ForeignKey(Instructor, on_delete=models.CASCADE, null=True, blank=True)

	@property
	def shamsi_register_date(self):
		return JalaliDatetime(self.register_date).strftime('%Y/%m/%d')

	def __str__(self):
		return f'{self.title} - {self.customer.full_name}'








