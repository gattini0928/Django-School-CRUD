from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .models import Teacher, Student, Exam, SchoolSubject
from .forms import TeacherForm, TeacherLoginForm, StudentForm
from django.views.generic import FormView, DetailView, ListView, CreateView, UpdateView, DeleteView
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin


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
        teacher = form.save(commit=False)
        teacher.user = user
        teacher.photo = self.request.FILES.get('photo')
        teacher.save()

        messages.success(self.request, "Account created with success! Login")
        return super().form_valid(form)

    def form_invalid(self, form):
        user_email = form.cleaned_data['email']
        messages.error(self.request, f'User {user_email} already Exists')
        return redirect('create_account')


class TeacherPerfilView(LoginRequiredMixin, DetailView):
    model = Teacher
    template_name = 'teacher_perfil.html'
    context_object_name = "teacher"

    def get_object(self):
        user = self.request.user
        teacher = Teacher.objects.filter(user=user).first()
        if not teacher:
            messages.warning(
                self.request, 'You need to be a teacher to see this profile.')
            return HttpResponseRedirect('/login/')
        return teacher


class TeacherUpdateView(LoginRequiredMixin, UpdateView):
    model = Teacher
    form_class = TeacherForm
    template_name = 'teacher_perfil.html'
    success_url = reverse_lazy('teacher_perfil')

    def get_object(self, queryset=None):
        teacher = get_object_or_404(Teacher, user=self.request.user)
        return teacher

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['teacher'] = self.get_object()
        return context

    def form_valid(self, form):
        teacher = form.save(commit=False)
        user = teacher.user
        user.username = form.cleaned_data['email']
        user.email = form.cleaned_data['email']
        user.save()
        teacher.photo = self.request.FILES.get('photo')
        teacher.save()

        messages.success(
            self.request, f'Perfil edited successfully, changes saved')
        return redirect('teacher_perfil')


@login_required
def delete_teacher(request, id):
    user = request.user
    teacher = get_object_or_404(Teacher, id=id, user=user)
    teacher.delete()
    user.delete()
    logout(request)
    messages.success(request, f"{user.username} deleted successfully")
    return redirect('create_account')


@login_required
def delete_student(request, id):
    student = get_object_or_404(Student, id=id)
    student.delete()
    messages.success(request, f"Student {student.name} deleted successfully")
    return redirect('students_perfil')


class StudentCreateAccountView(LoginRequiredMixin, FormView):
    form_class = StudentForm
    template_name = 'create_student.html'
    success_url = reverse_lazy('students_perfil')

    def form_valid(self, form):
        user = User.objects.create_user(
            username=form.cleaned_data['email'],
            email=form.cleaned_data['email'],
            password=form.cleaned_data['password'],
        )

        student = form.save(commit=False)
        student.user = user
        student.photo = self.request.FILES.get('photo')
        student.save()

        messages.success(self.request, "Student created with success!")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if 'student' in kwargs:
            context['student'] = kwargs['student']
            context['subjects'] = kwargs['subjects']
        return context


class StudentsPerfilView(LoginRequiredMixin, ListView):
    model = Student
    template_name = 'students_perfil.html'
    context_object_name = "students"


@login_required
def user_logout(request):
    user = request.user
    logout(request)
    messages.info(request, f'User {user.username} logout successfully')
    return redirect('index')
