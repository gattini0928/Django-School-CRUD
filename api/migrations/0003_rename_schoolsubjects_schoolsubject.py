# Generated by Django 5.1.6 on 2025-02-12 18:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_remove_student_user_schoolsubjects'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='SchoolSubjects',
            new_name='SchoolSubject',
        ),
    ]
