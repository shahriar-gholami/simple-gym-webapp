from django.urls import path, include
from . import views
from django.apps import apps

current_app_name = apps.get_containing_app_config(__name__).name



app_name = f"{current_app_name}"

urlpatterns = [
    
    path('', views.CustomerRegister.as_view(), name='index'),
    path('course-register/', views.CourseRegisterView.as_view(), name='course_register'),
    path('delete-customer/<int:customer_id>/', views.DeleteCustomerView.as_view(), name='delete_customer'),
    path('finance/instructor/<int:instructor_id>/', views.InstructorFinanceView.as_view(), name='instructor_finance'),
    path('payments/', views.SubmitPaymentsView.as_view(), name='payments'),
    path('instructor-dept-pay/', views.ConfirmInstructorPaymentView.as_view(), name='instructor_dept_pay'),
    path('submit-gym-costs/', views.SubmitGymCostsView.as_view(), name='submit_gym_costs'),
    path('instructors/', views.InstructorsView.as_view(), name='instructors'),
    path('courses/', views.CoursesView.as_view(), name='courses'),
   ]