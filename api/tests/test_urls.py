from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse
from api.models import Teacher, Student


class AuthenticatedUrlsTestCase(TestCase):
    def setUp(self):
        self.client = Client()

        self.teacher_user = get_user_model().objects.create_user(
            username='JoaoAlano', password='123456')
        self.student_user = get_user_model().objects.create_user(
            username='ChicoBoarte', password='123456')

        self.teacher = Teacher.objects.create(
            user=self.teacher_user,
            name='Joao Alano',
            email='joaoalano1710@gmail.com',
            school_subject='Arts')
        self.student = Student.objects.create(
            user=self.student_user,
            name='Chico Boarte',
            email='chicoboarte@gmail.com',
            student_status=True)

        self.client.login(username='JoaoAlano', password='123456')

    def test_index_url(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)

    def test_students_url(self):
        response = self.client.get(reverse('students_perfil'))
        self.assertEqual(response.status_code, 200)

    def test_exam_manager_url(self):
        url = reverse('exam_manager', kwargs={
                      'student_id': self.student.id, 'teacher_id': self.teacher.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_create_account_url(self):
        response = self.client.get(reverse('create_account'))
        self.assertEqual(response.status_code, 200)

    def test_login_url(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)

    def test_teacher_perfil_url(self):
        response = self.client.get(reverse('teacher_perfil'))
        self.assertEqual(response.status_code, 200)

    def test_edit_perfil_url(self):
        response = self.client.get(reverse('teacher_edit_perfil'))
        self.assertEqual(response.status_code, 200)

    def test_teachers_url(self):
        response = self.client.get(reverse('teachers'))
        self.assertEqual(response.status_code, 200)

    def test_teacher_exams_url(self):
        response = self.client.get(reverse('teacher_exams'))
        self.assertEqual(response.status_code, 200)

    def test_teacher_delete_url(self):
        url = reverse('delete_teacher', kwargs={'id': self.teacher.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

    def test_student_create_url(self):
        response = self.client.get(reverse('create_student'))
        self.assertEqual(response.status_code, 200)

    def test_students_grades_url(self):
        url = reverse('student_grades', kwargs={'id': self.student.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_student_delete_url(self):
        url = reverse('delete_student', kwargs={'id': self.student.id})
        response = self.client.get(url)
        # Esperado redirecionamento
        self.assertEqual(response.status_code, 302)

    def test_logout(self):
        self.client.logout()
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)

    def test_not_user(self):
        self.client.logout()
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 302)

    def test_url_not_exist(self):
        response = self.client.get('/dashboard/') 
        self.assertEqual(response.status_code, 404)

    def test_exam_manager_invalid_ids(self):
        url = reverse('exam_manager', kwargs={
                      'student_id': 999, 'teacher_id': 888})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
