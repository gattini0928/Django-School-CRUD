from api.models import Teacher, Student
from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse


class ViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.teacher_user = get_user_model().objects.create_user(
            username='professor', password='123456')
        self.student_user = get_user_model().objects.create_user(
            username='aluno', password='123456')

        self.teacher = Teacher.objects.create(
            user=self.teacher_user, name='Professor', email='prof@email.com', school_subject='Mathematics')
        self.student = Student.objects.create(
            user=self.student_user, name='Aluno', email='aluno@email.com', student_status=True)

    def test_index_view(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 302)

    def test_teacher_perfil_view_authenticated(self):
        self.client.login(username='professor', password='123456')
        response = self.client.get(reverse('teacher_perfil'))
        self.assertEqual(response.status_code, 200)

    def test_teacher_perfil_view_unauthenticated(self):
        response = self.client.get(reverse('teacher_perfil'))
        self.assertEqual(response.status_code, 302)

    def test_exam_manager_view(self):
        self.client.login(username='professor', password='123456')
        url = reverse('exam_manager', kwargs={
                      'student_id': self.student.id, 'teacher_id': self.teacher.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_exam_manager_invalid_ids(self):
        self.client.login(username='professor', password='123456')
        url = reverse('exam_manager', kwargs={
                      'student_id': 999, 'teacher_id': 888})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_logout_redirect(self):
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 302)

    def test_index_uses_correct_template(self):
        self.client.login(username='professor', password='123456')
        response = self.client.get(reverse('index'))
        self.assertTemplateUsed(response, 'index.html')

    def test_unauthenticated_uses_correct_template(self):
        response = self.client.get(reverse('index'), follow=True)
        self.assertTemplateUsed(response, 'login.html')
