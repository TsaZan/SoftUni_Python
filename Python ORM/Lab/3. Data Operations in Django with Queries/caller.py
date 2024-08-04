import os
import django

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

from main_app.models import Student


# def add_students():
#     Student.objects.create(
#         student_id='FC5204',
#         first_name='John',
#         last_name='Doe',
#         birth_date='1995-05-15',
#         email='john.doe@university.com',
#     )
#     Student.objects.create(
#         student_id='FE0054',
#         first_name='Jane',
#         last_name='Smith',
#         email='jane.smith@university.com', )
#
#     Student.objects.create(
#         student_id='FH2014',
#         first_name='Alice',
#         last_name='Johnson',
#         birth_date='1998-02-10',
#         email='alice.johnson@university.com',
#     )
#
#     Student.objects.create(
#         student_id='FH2015',
#         first_name='Bob',
#         last_name='Wilson',
#         birth_date='1996-11-25',
#         email='bob.wilson@university.com',
#     )

def get_students_info():
    students = Student.objects.all()
    result = [(f'Student №{student.student_id}: {student.first_name} '
               f'{student.last_name}; Email: {student.email}') for student in students]
    return '\n'.join(result)


def update_students_emails():
    students = Student.objects.all()

    for s in students:
        new_mail = s.email.replace('university.com', 'uni-students.com')
        s.email = new_mail
        s.save()


def truncate_students():
    Student.objects.all().delete()

# print(get_students_info())

# update_students_emails()
# for student in Student.objects.all():
#     print(student.email)

# truncate_students()
# print(Student.objects.all())
# print(f"Number of students: {Student.objects.count()}")
