from django.db import models
from django.utils.translation import gettext_lazy as _
from khayyam import JalaliDatetime


class CourseTitle(models.Model):
	title = models.CharField(max_length=250)

	def __str__(self):
		return f'{self.title}'

class Customer(models.Model):
	full_name = models.CharField(max_length=30, unique=True)
	create_date = models.DateTimeField(auto_now_add = True)
	phone_number = models.CharField(max_length=250)

	@property
	def register_date(self):
		return JalaliDatetime(self.create_date).strftime('%Y/%m/%d')
	
	def __str__(self):
		return f'{self.full_name}'

class ReservedCourse(models.Model):
	title = models.ForeignKey(CourseTitle, on_delete=models.CASCADE)
	customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
	num_of_sessions = models.IntegerField(default=0)
	cost_paid = models.IntegerField(default=0)
	register_date = models.CharField(max_length=250)

	def get_register_day(self):
		from_time_words=self.register_date.split()
		if from_time_words[1] == 'شنبه':
			from_time_day = int(from_time_words[2])
		else:
			from_time_day = int(from_time_words[1])
		return from_time_day

	def get_register_month(self):
		months_dict = {
						'فروردین': 1,
						'اردیبهشت': 2,
						'خرداد': 3,
						'تیر': 4,
						'مرداد': 5,
						'شهریور': 6,
						'مهر': 7,
						'آبان': 8,
						'آذر': 9,
						'دی': 10,
						'بهمن': 11,
						'اسفند': 12
					}
		register_time_words=self.register_date.split()
		if register_time_words[2] in months_dict:
			register_time_month = months_dict[register_time_words[2]]
		elif register_time_words[3] in months_dict:
			register_time_month = months_dict[register_time_words[3]]
		return register_time_month

	def get_register_year(self):
		register_time_words=self.register_date.split()
		if register_time_words[3].isdigit():
			register_time_year = int(register_time_words[3])
		else:
			register_time_year = int(register_time_words[4])
		return register_time_year

	def __str__(self):
		return f'{self.title} - {self.customer.full_name}'
