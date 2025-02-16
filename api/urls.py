from django.urls import path
from .views import *
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', index, name='index'),
    path('create-account/', TeacherCreateAccountView.as_view(),
         name='create_account'),
    path('login/', TeacherLoginView.as_view(), name='login'),
    path('logout/', user_logout, name='logout'),
    path('create-student/', StudentCreateAccountView.as_view(),
         name='create_student'),
    path('teacher-perfil/', TeacherPerfilView.as_view(),
         name='teacher_perfil'),
    path('students/', StudentsPerfilView.as_view(),
         name='students_perfil'),

]
