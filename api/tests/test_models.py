from django.test import TestCase
from api.models import Student, Exam, Teacher
from django.contrib.auth import get_user_model
from datetime import date

class TeacherModelTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create(username='Gabriel')
        self.teacher = Teacher.objects.create(
            user=self.user,
            name='Gabriel Gattini',
            email='gabrielgattini0928659@yahoo.com',
            school_subject='Computer Science'
        )

    def test_teacher_creation(self):
        self.assertEqual(self.teacher.name, 'Gabriel Gattini')
        self.assertEqual(self.teacher.email, 'gabrielgattini0928659@yahoo.com')
        self.assertEqual(self.teacher.school_subject, 'Computer Science')

    def test_teacher_str(self):
        self.assertEqual(str(self.teacher),
                         'Teacher Gabriel Gattini - Subject Computer Science')

    def test_teacher_get_photo_url(self):
        self.assertEqual(self.teacher.get_photo_url(),
                         '/media/teachers/default.jpg')

        self.teacher.photo = 'teachers/profile1.jpg'
        self.teacher.save()
        self.assertEqual(self.teacher.get_photo_url(),
                         '/media/teachers/profile1.jpg')

    def test_teacher_change_password(self):
        new_password = '1234user'
        self.user.set_password(new_password)
        self.user.save()

        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password(new_password))


class StudentModelTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create(username='Katia Victoria')
        self.student = Student.objects.create(
            user=self.user,
            name='Katia Victoria',
            email='gabrielgattini0928659@yahoo.com',
            student_status=False
        )
        self.teacher1 = Teacher.objects.create(
            user=get_user_model().objects.create(username='Everton'),
            name='Everton Cazares',
            email='evertoncazares659@gmail.com',
            school_subject='Chemistry')

        self.teacher2 = Teacher.objects.create(
            user=get_user_model().objects.create(username='Obereto'),
            name='Obereto Raimundus',
            email='oberetoraimundus@gmail.com',
            school_subject='Arts')

    def test_add_teachers_to_student(self):
        self.student.teachers.add(self.teacher1, self.teacher2)
        self.assertEqual(self.student.teachers.count(), 2)

    def test_remove_teacher_from_student(self):
        self.student.teachers.add(self.teacher1, self.teacher2)
        self.student.teachers.remove(self.teacher1)
        self.assertEqual(self.student.teachers.count(), 1)

    def test_clear_teachers_from_student(self):
        self.student.teachers.add(self.teacher1, self.teacher2)
        self.student.teachers.clear()
        self.assertEqual(self.student.teachers.count(), 0)

    def test_student_get_photo_url(self):
        self.assertEqual(self.student.get_photo_url(),
                         '/media/students/default.jpg')

        self.student.photo = 'students/profile1.jpg'
        self.student.save()
        self.assertEqual(self.student.get_photo_url(),
                         '/media/students/profile1.jpg')

    def test_student_status(self):
        self.assertEqual(self.student.student_status, False)


class ExamModelTest(TestCase):
    def setUp(self):
        self.teacher = Teacher.objects.create(
            user=get_user_model().objects.create(username='Cleiton'),
            name='Cleiton Ribeiro',
            email='cleitonribeiro@gmail.com',
            school_subject='English'
        )
        self.teacher2 = Teacher.objects.create(
            user=get_user_model().objects.create(username='Aruan'),
            name='Aruan Mauricio',
            email='aruan123@gmail.com',
            school_subject='Mathematics'
        )
        self.student = Student.objects.create(
            user=get_user_model().objects.create(username='Gabriel'),
            name='Gabriel Elgert Gattini',
            email='gabriel123@gmail.com',
            student_status=True
        )

        self.student.teachers.set([self.teacher])

        self.exam = Exam.objects.create(
            student=self.student,
            teacher=self.teacher,
            subject='English',
            grade=8.8
        )
        self.exam1 = Exam.objects.create(
            student=self.student,
            teacher=self.teacher,
            subject='English',
            grade=10
        )

        self.exam2 = Exam.objects.create(
            student=self.student,
            teacher=self.teacher,
            subject='English',
            grade=10
        )
        self.exam3 = Exam.objects.create(
            student=self.student,
            teacher=self.teacher,
            subject='English',
            grade=10
        )
        self.exam4 = Exam.objects.create(
            student=self.student,
            teacher=self.teacher,
            subject='English',
            grade=10
        )
        self.exam5 = Exam.objects.create(
            student=self.student,
            teacher=self.teacher,
            subject='English',
            grade=10
        )
        self.exam6 = Exam.objects.create(
            student=self.student,
            teacher=self.teacher,
            subject='English',
            grade=10
        )

        self.exam7 = Exam.objects.create(
            student=self.student,
            teacher=self.teacher,
            subject='English',
            grade=1.2
        )

        self.exam_reproved = Exam.objects.create(
            student=self.student,
            teacher=self.teacher2,
            subject='Mathematics',
            grade=60)

    def test_get_grades_by_subject(self):
        grades = self.student.get_grades_by_subject()

        expected_avg = round((10 * 6 + 8.8 + 1.2) / 8, 2)
        expected_total = min(10 * 6 + 8.8 + 1.2, 100)

        self.assertEqual(grades['English']['average'], expected_avg)
        self.assertEqual(grades['English']['total_score'], expected_total)
        self.assertEqual(grades['English']['status'], True)

        self.assertEqual(grades['Mathematics']['average'], 60)
        self.assertEqual(grades['Mathematics']['total_score'], 60)
        self.assertEqual(grades['Mathematics']['status'], False)

    def test_exam_date_auto_set(self):
        self.assertEqual(self.exam.date, date.today())
