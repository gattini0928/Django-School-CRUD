from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .models import Teacher
from .forms import TeacherForm, TeacherLoginForm
from django.views.generic import FormView
from django.contrib import messages
from django.contrib.auth.decorators import login_required


def index(request):
    return render(request, 'index.html')

class TeacherLoginView(FormView):
    model = Teacher
    template_name = "login.html"
    success_url = reverse_lazy('index')
    form_class = TeacherLoginForm

    def form_valid(self, form):
        email = form.cleaned_data['email']
        password = form.cleaned_data['password']
        user = authenticate(self.request, username=email, password=password)
        if user is not None:
            login(self.request, user)
            messages.success(self.request, f'Welcome {user.username}')
            return super().form_valid(form)
        else:
            messages.error(
                self.request, 'Invalid Credentials. Try again.')
            return self.form_invalid(form)


class TeacherCreateAccountView(FormView):
    form_class = TeacherForm
    template_name = 'create_account.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        user = User.objects.create_user(
            username=form.cleaned_data['email'],
            email=form.cleaned_data['email'],
            password=form.cleaned_data['password'],
        )
        Teacher.objects.create(
            user=user,
            name=form.cleaned_data['name'],
            email=form.cleaned_data['email'],
            school_subject=form.cleaned_data['school_subject']
        )
        messages.success(self.request, "Account created with success! Login")
        return super().form_valid(form)


@login_required
def user_logout(request):
    user = request.user
    logout(request)
    messages.info(request, f'User {user.username} logout successfully')
    return redirect('index')
