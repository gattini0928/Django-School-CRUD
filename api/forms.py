from django import forms
from .models import Teacher, Exam, Student
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.contrib import messages


class TeacherForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'form-input', 'placeholder': 'Password'}),
        required=False)

    class Meta:
        model = Teacher
        fields = ['name', 'email', 'password', 'school_subject', 'photo']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Nome'}),
            'email': forms.EmailInput(attrs={'class': 'form-input', 'placeholder': 'Email'}),
            'school_subject': forms.Select(attrs={'class': 'form-input'}),
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exclude(pk=self.instance.user.pk).exists():
            raise ValidationError('This email is already in use.')
        return email

    def save(self, commit=True):
        teacher = super().save(commit=False)

        if not teacher.user:
            teacher.user = User.objects.create(
                username=self.cleaned_data['email'], email=self.cleaned_data['email'])

        if self.cleaned_data['password']:
            teacher.user.set_password(self.cleaned_data['password'])

        if commit:
            teacher.user.save()
            teacher.save()

        return teacher


class TeacherLoginForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(
        attrs={'class': 'form-input', 'placeholder': 'Email'}))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'form-input', 'placeholder': 'Password'}))


class StudentForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'form-input', 'placeholder': 'Password'}))

    class Meta:
        model = Student
        fields = ['name', 'email', 'password', 'photo']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Nome'}),
            'email': forms.EmailInput(attrs={'class': 'form-input', 'placeholder': 'Email'}),
        }


class ExamForm(forms.ModelForm):
    class Meta:
        model = Exam
        fields = ['student', 'teacher', 'subject', 'grade']
