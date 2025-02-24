from django import forms
from .models import Teacher, Exam, Student


class TeacherForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'form-input', 'placeholder': 'Password'}),
        required=True)

    class Meta:
        model = Teacher
        fields = ['name', 'email', 'password', 'school_subject', 'photo']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Nome', 'required': True}),
            'email': forms.EmailInput(attrs={'class': 'form-input', 'placeholder': 'Email', 'required': True}),
            'school_subject': forms.Select(attrs={'class': 'form-input', 'required': True}),
        }


class TeacherLoginForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(
        attrs={'class': 'form-input', 'placeholder': 'Email'}))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'form-input', 'placeholder': 'Password'}))


class TeacherUpdateForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'form-input', 'placeholder': 'Password'}),
        required=False)

    class Meta:
        model = Teacher
        fields = ['name', 'email', 'password', 'photo']

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Nome',  'required': False}),
            'email': forms.EmailInput(attrs={'class': 'form-input', 'placeholder': 'Email', 'required': False}),
        }


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
