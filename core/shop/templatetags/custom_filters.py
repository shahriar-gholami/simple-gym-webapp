from django import template

register = template.Library()

@register.filter
def monthly_income(instructor, arg):
    """
    فیلتر برای فراخوانی متد get_monthly_income با آرگومان‌ها
    :param instructor: شیء Instructor
    :param arg: رشته‌ای به فرمت 'year,month' (مثلاً '1402,1')
    :return: نتیجه متد get_monthly_income
    """
    year, month = map(int, arg.split(','))
    return instructor.get_monthly_income(year, month)