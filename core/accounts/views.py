from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.views import View
from .forms import CustomLoginForm
from django.contrib import messages

class CustomLoginView(View):
    form_class = CustomLoginForm
    template_name = 'accounts/login.html'

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            phone = form.cleaned_data['phone_number']
            password = form.cleaned_data['password']
            user = authenticate(request, phone_number=phone, password=password)

            if user is not None:
                login(request, user)
                return redirect('shop:course_register')  # به دلخواه تغییر بده
            else:
                messages.error(request, 'Phone number or password is incorrect.')
                message = 'نام کاربری یا رمز عبور نامعتبر'

        return render(request, self.template_name, {'form': form, 'message':message})


class LogoutView(View):

	def get(self, request):
		logout(request)
		return redirect('accounts:login')
