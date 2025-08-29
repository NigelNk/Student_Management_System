from django.core.management.base import BaseCommand
from profiles.models import Student, Subject, Grade

FORM_MAP = {
    'Form 1': 1,
    'Form 2': 2,
    'Form 3': 3,
    'Form 4': 4,
}

class Command(BaseCommand):
    help = 'Generate empty grade records for all students based on their form and matching subjects.'

    def handle(self, *args, **kwargs):
        students = Student.objects.all()
        subjects = Subject.objects.all()

        if not students.exists():
            self.stdout.write(self.style.WARNING("No students found."))
            return

        if not subjects.exists():
            self.stdout.write(self.style.WARNING("No subjects found."))
            return

        grade_count = 0

        for student in students:
            form_number = FORM_MAP.get(student.form)
            if not form_number:
                self.stdout.write(self.style.WARNING(f"Student {student} has invalid form: {student.form}"))
                continue

            matching_subjects = subjects.filter(subject_form=form_number)

            for subject in matching_subjects:
                # Avoid duplicate grades
                if not Grade.objects.filter(student=student, subject=subject).exists():
                    Grade.objects.create(
                        student=student,
                        subject=subject,
                        ca1=0,
                        ca2=0,
                        et=0,
                        grade='-',
                        remark='-'
                    )
                    grade_count += 1
                    self.stdout.write(self.style.SUCCESS(f"Created grade for {student} in {subject}"))

        self.stdout.write(self.style.SUCCESS(f"\nSuccessfully created {grade_count} grade(s)."))
