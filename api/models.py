from django.db import models
from django.contrib.auth.models import User

SCHOOL_SUBJECTS_CHOICES = [
    ("Mathematics", "Mathematics"),
    ("English", "English"),
    ("Literature", "Literature"),
    ("History", "History"),
    ("Sciences", "Sciences"),
    ("Arts", "Arts"),
    ("Chemistry", "Chemistry"),
    ("Physics", "Physics"),
    ("Biology", "Biology"),
    ("Philosophy", "Philosophy"),
    ("Computer Science", "Computer Science"),
    ("Geography", "Geography"),

]

class Teacher(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, blank=True, default=None)
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    school_subject = models.CharField(
        max_length=50, choices=SCHOOL_SUBJECTS_CHOICES)
    photo = models.ImageField(upload_to='teachers/', null=True, blank=True)

    def __str__(self):
        return f'Teacher {self.name} - Subject {self.school_subject}'


class Student(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, blank=True, default=None)
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    photo = models.ImageField(upload_to='students/', null=True, blank=True)

    teachers = models.ForeignKey(
        Teacher, on_delete=models.SET_NULL, related_name='students', null=True, blank=True)

    def save(self, *args, **kwargs):
        """Automatically creates all subjects for the student."""
        super().save(*args, **kwargs)  # Salva o aluno primeiro
        for subject in SCHOOL_SUBJECTS_CHOICES:
            SchoolSubject.objects.get_or_create(
                student=self, subject=subject[0])

    def total_score(self):
        """Calculates the sum of all grades and ensures that it does not exceed 100."""
        total = sum(subject.grade for subject in self.subjects.all())
        return min(total, 100)

    def total_score_by_subject(self):
        """Returns a dictionary with the sum of grades per subject."""
        subject_scores = {}
        for subject in SCHOOL_SUBJECTS_CHOICES:
            subject_name = subject[0]
            exams = Exam.objects.filter(student=self, subject=subject_name)
            total = sum(exam.grade for exam in exams)
            subject_scores[subject_name] = min(
                total, 100)
        return subject_scores

    @property
    def status(self):
        """Returns the student's status based on the accumulated grade."""
        final_grade = self.total_score()
        if final_grade >= 65:
            return 'Student Approved'
        elif final_grade >= 55:
            return 'Student in Recuperation'
        else:
            return 'Student Reproved'

    def __str__(self):
        return self.name


class SchoolSubject(models.Model):
    student = models.ForeignKey(
        Student, on_delete=models.CASCADE, related_name='subjects')
    subject = models.CharField(max_length=50, choices=SCHOOL_SUBJECTS_CHOICES)
    grade = models.DecimalField(
        max_digits=4, decimal_places=2, default=0.0)

    def __str__(self):
        return f"{self.subject} - {self.student.name}: {self.grade}"


class Exam(models.Model):
    student = models.ForeignKey(
        Student, on_delete=models.CASCADE, related_name="exams")
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    subject = models.CharField(max_length=50, choices=SCHOOL_SUBJECTS_CHOICES)
    grade = models.DecimalField(max_digits=4, decimal_places=2)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.subject} - {self.student.name}: {self.grade}"
