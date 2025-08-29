from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from profiles.models import Student, Subject, Grade  # adjust this if needed
from faker import Faker
import random

fake = Faker()
User = get_user_model()

SEX = ['Male', 'Female']
FORMS  = [
    (None, None),
    ('Form 1', 'Form One'),
    ('Form 2', 'Form Two'),
    ('Form 3', 'Form Three'),
    ('Form 4', 'Form Four'),
]
STREAMS = ['A', 'B', 'C']

# Remove (None, None) option
VALID_FORMS = [f[0] for f in FORMS if f[0] is not None]
VALID_STREAMS = STREAMS  # already valid

class Command(BaseCommand):
    help = 'Create fake student users with profiles'

    def add_arguments(self, parser):
        parser.add_argument('--count', type=int, default=10, help='Number of students to create')

    def handle(self, *args, **options):
        count = options['count']
        subjects = list(Subject.objects.all())

        for _ in range(count):
            email = fake.unique.email()
            username = email.split('@')[0]
            first_name = fake.first_name()
            last_name = fake.last_name()

            user = User.objects.create_user(
                username=username,
                email=email,
                password='testpass123',
                role='student',
                first_name=first_name,
                last_name=last_name,
            )

            student = Student.objects.create(
                user=user,
                student_id=f"S{random.randint(10000, 99999)}",
                gender=random.choice(SEX),
                dob=fake.date_of_birth(minimum_age=13, maximum_age=18),
                form=random.choice(VALID_FORMS),      # will never be None
                stream=random.choice(VALID_STREAMS),  # will never be None
                joined_school_at=fake.date_this_decade(),
                guardian_name=fake.name(),
                guardian_phone=fake.phone_number(),
                guardian_email=fake.unique.email(),
                address=fake.address()
            )

            student.subject.set(random.sample(subjects, k=min(3, len(subjects))))


            self.stdout.write(self.style.SUCCESS(f"Created student user: {username}"))

        self.stdout.write(self.style.SUCCESS(f"\nSuccessfully created {count} fake student(s)."))
