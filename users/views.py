from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from django.urls import reverse_lazy
from django.views.generic import FormView

from users.forms import LoginForm, UserCreationForm


# def login_view(request):
# #     form = ''
# #     context = {
# #         "title": "Login | Rental Exchange",
# #         "form": form
# #     }
# #     return render(request, 'rental_exchange/containers/login.html', context)
# #
# #
def register_view(request):
    form = UserCreationForm
    context = {
        "title": "Registration | Rental Exchange",
        "form": form
    }
    return render(request, 'rental_exchange/containers/signup.html', context)


class SignupView(FormView):
    """sign up user view"""
    form_class = UserCreationForm
    template_name = 'rental_exchange/containers/signup.html'
    success_url = reverse_lazy('home')
    success_message = 'Your Registration Has Been Completed Successfully'

    def form_valid(self, form):
        """ process user signup"""
        user = form.save(commit=False)
        user.user_type = 'Customer'
        user.save()
        messages.success(self.request, 'Your Registration Has Been Completed Successfully')
        login(self.request, user)
        if user is not None:
            return HttpResponseRedirect(self.success_url)

        return super().form_valid(form)


class LoginView(FormView):
    """login view"""

    form_class = LoginForm
    success_url = reverse_lazy('home')
    template_name = 'rental_exchange/containers/login.html'

    def form_valid(self, form):
        """ process user login"""
        credentials = form.cleaned_data

        user = authenticate(username=credentials['email'],
                            password=credentials['password'])
        if user is not None and user.user_type == 'Customer':
            login(self.request, user)
            messages.add_message(self.request, messages.SUCCESS, 'You are logged in successfully')
            return HttpResponseRedirect(self.success_url)

        else:
            messages.add_message(self.request, messages.ERROR, 'Wrong credentials\
                                please try again')
            return HttpResponseRedirect(reverse_lazy('login'))


def logout_view(request):
    """logout logged in user"""
    logout(request)
    return HttpResponseRedirect(reverse_lazy('home'))


class AdminLoginView(FormView):
    """login view"""

    form_class = LoginForm
    success_url = reverse_lazy('admin-home')
    template_name = 'rental_exchange/admin/containers/login.html'

    def form_valid(self, form):
        """ process user login"""
        credentials = form.cleaned_data

        user = authenticate(username=credentials['email'],
                            password=credentials['password'])
        if user is not None and user.is_staff:
            login(self.request, user)
            messages.add_message(self.request, messages.SUCCESS, 'You are logged in successfully')
            return HttpResponseRedirect(self.success_url)

        else:
            messages.add_message(self.request, messages.ERROR, 'Wrong credentials\
                                please try again')
            return HttpResponseRedirect(reverse_lazy('admin-login'))