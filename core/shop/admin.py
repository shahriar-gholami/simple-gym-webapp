from django.contrib import admin
from.models import *


class ReservedCourseInline(admin.TabularInline):
    model = ReservedCourse
    extra = 0  # تعداد ردیف‌های اضافی که نمایش داده می‌شود
    fields = ['title', 'num_of_sessions', 'cost_paid', 'register_date']
    readonly_fields = ['register_date']  # اگر نمی‌خواهید برخی فیلدها قابل ویرایش باشند
    show_change_link = True  # برای ایجاد لینک به جزئیات ReservedCourse

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'phone_number', 'register_date']
    search_fields = ['full_name', 'phone_number']
    inlines = [ReservedCourseInline]

@admin.register(ReservedCourse)
class ReservedCourseAdmin(admin.ModelAdmin):
    list_display = ['title', 'customer', 'num_of_sessions', 'cost_paid', 'register_date']
    search_fields = ['customer__full_name', 'title__name']

class CourseTitleAdmin(admin.ModelAdmin):
    list_display = ['title',]
    search_fields = ['title',]

admin.site.register(CourseTitle, CourseTitleAdmin)


