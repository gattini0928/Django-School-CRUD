from api.forms import TeacherForm
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile


class TeacherFormTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create(username='Robert')

    def test_teacher_form_valid(self):
        with open('media/teachers/blanco1.jpg', 'rb') as img_file:
            photo = SimpleUploadedFile(
                img_file.name, img_file.read(), content_type='image/jpeg')

        form = TeacherForm(data={
            'name': 'Roberto Blanco',
            'email': 'robertoelblanco@icloud.com',
            'password': '123456',
            'school_subject': 'Computer Science',
        }, files={
            'photo': photo
        })

        form2 = TeacherForm(data={
            'name': 'Roberto Blanco',
            'email': 'robertoelblanco@icloud.com',
            'password': '',
            'school_subject': 'Computer Science',
        }, files={
            'photo': photo
        })

        self.assertTrue(form2.is_valid(), msg=form.errors)
