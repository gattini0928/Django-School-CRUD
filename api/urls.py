from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name='index'),
    path('exam-manager/<int:student_id>/<int:teacher_id>/', exam_manager, name='exam_manager'),
    path('create-account/', TeacherCreateAccountView.as_view(),
         name='create_account'),
    path('login/', TeacherLoginView.as_view(), name='login'),
    path('teacher-perfil/', TeacherPerfilView.as_view(),
         name='teacher_perfil'),
    path('teacher-edit-perfil/', TeacherUpdateView.as_view(),
         name='teacher_edit_perfil'),
    path('delete-teacher/<int:id>/',
         delete_teacher, name='delete_teacher'),

    path('create-student/', StudentCreateAccountView.as_view(),
         name='create_student'),
    path('students/', StudentsPerfilView.as_view(),
         name='students_perfil'),
    path('student-grades/<int:id>', StudentGradeView.as_view(),
         name='student_grades'),
    path('delete-student/<int:id>/',
         delete_student, name='delete_student'),
    path('logout/', user_logout, name='logout'),

]
