from django.test import TestCase

from django.test import TestCase
from main_app.models import Lecturer, Subject, Student, StudentEnrollment
from django.db import models

class StudentSubjectModelTest(TestCase):
    # Contests tests
    def setUp(self):
        # Create lecturers
        self.lecturer1 = Lecturer.objects.create(first_name="John", last_name="Doe")
        self.lecturer2 = Lecturer.objects.create(first_name="Jane", last_name="Smith")

        # Create subjects and associate with lecturers
        self.mathematics = Subject.objects.create(name="Mathematics", code="MATH101", lecturer=self.lecturer1)
        self.history = Subject.objects.create(name="History", code="HIST101", lecturer=self.lecturer2)
        self.physics = Subject.objects.create(name="Physics", code="PHYS101", lecturer=self.lecturer1)

        # Create students
        self.student1 = Student.objects.create(
            student_id="M1051",
            first_name="Alice",
            last_name="Johnson",
            birth_date="2000-01-15",
            email="a.johnson@abv.bg"
        )
        self.student2 = Student.objects.create(
            student_id="S217",
            first_name="Bob",
            last_name="Smith",
            birth_date="2001-05-20",
            email="bobby@gmail.com"
        )

    def test_student_enrollments(self):
        self.student2.subjects.add(self.mathematics)
        self.student2.subjects.add(self.physics)
        self.student2.subjects.add(self.history)
        student = Student.objects.get(student_id="S217")

        # Retrieve the student's enrollments
        enrollments = student.studentenrollment_set.all()

        # Check if the student is enrolled in 3 subjects
        self.assertEqual(len(enrollments), 3)