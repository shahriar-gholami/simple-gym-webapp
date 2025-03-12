from django.contrib import admin
from.models import *


class ReservedCourseInline(admin.TabularInline):
    model = ReservedCourse
    extra = 0  
    fields = ['title', 'num_of_sessions', 'cost_paid', 'register_date']
    readonly_fields = ['register_date'] 
    show_change_link = True  

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'phone_number', 'create_date', 'ensurance')
    search_fields = ('full_name', 'phone_number', 'national_code')
    list_filter = ('ensurance', 'create_date')

@admin.register(ReservedCourse)
class ReservedCourseAdmin(admin.ModelAdmin):
    list_display = ['title', 'customer', 'num_of_sessions', 'cost_paid', 'shamsi_register_date']
    search_fields = ['customer__full_name', 'title__name']

class CourseTitleAdmin(admin.ModelAdmin):
    list_display = ['title',]
    search_fields = ['title',]

admin.site.register(CourseTitle, CourseTitleAdmin)

@admin.register(Instructor)
class InstructorAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'phone_number', 'national_code', 'created_date')
    list_filter = ('created_date',)
    search_fields = ('full_name', 'national_code')
    filter_horizontal = ('courses',)  # برای نمایش بهتر ManyToManyField

@admin.register(InstructorMonthlyIncome)
class InstructorMonthlyIncomeAdmin(admin.ModelAdmin):
    list_display = ('instructor', 'month', 'year', 'get_monthly_income')
    search_fields = ('instructor', )
    filter_horizontal = ('courses',)  # برای نمایش بهتر ManyToManyField
