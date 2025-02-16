from django import forms
from .models import Teacher, Exam, Student


class TeacherForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'form-input', 'placeholder': 'Password'}))

    class Meta:
        model = Teacher
        fields = ['name', 'email', 'password', 'school_subject', 'photo']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Nome'}),
            'email': forms.EmailInput(attrs={'class': 'form-input', 'placeholder': 'Email'}),
            'school_subject': forms.Select(attrs={'class': 'form-input'}),
        }


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


class StudentLoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput())


class ExamForm(forms.ModelForm):
    class Meta:
        model = Exam
        fields = ['student', 'teacher', 'subject', 'grade']
