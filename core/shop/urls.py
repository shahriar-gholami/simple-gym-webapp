from django.urls import path, include
from . import views
from django.apps import apps

current_app_name = apps.get_containing_app_config(__name__).name



app_name = f"{current_app_name}"

urlpatterns = [
    
    path('', views.CustomerRegister.as_view(), name='index'),
    path('course-register', views.CourseRegisterView.as_view(), name='course_register'),
    
   ]