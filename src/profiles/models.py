from datetime import date
from django.db import models
from django.db.models import Count

from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth import get_user_model

SEX = [
    ('male', 'Male'),
    ('female', 'Female'),
]

FORMS  = [
    (None, None),
    ('Form 1', 'Form One'),
    ('Form 2', 'Form Two'),
    ('Form 3', 'Form Three'),
    ('Form 4', 'Form Four'),
]

STREAMS = [
    (None, None),
    ('A', 'A'),
    ('B', 'B'),
]

MARITAL_STATUS  = [
    ('Single', 'Single'),
    ('Married', 'Married')
]

class Subject(models.Model):
    subject_name = models.CharField(max_length=30)
    subject_form = models.PositiveIntegerField(verbose_name='Form',null=True, validators=[MaxValueValidator(4), MinValueValidator(1)])
    subject_bio  = models.TextField(blank=True, null=True)

    @property
    def subject_code(self):
        subject = self.subject_name

        if subject == 'biology'.capitalize() or subject == 'geography'.capitalize():
            code = subject[:3] + "-" + str(self.subject_form)

        else:
            code = subject[:4] + "-" + str(self.subject_form)

        return code
    
    @property
    def subject_full_form_name(self):
        return f"Form {self.subject_form}"
    

    def __str__(self):
        return f"{self.subject_name} (Form {self.subject_form})"


class Student(models.Model):
    # student info
    user                    = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    student_id              = models.CharField(max_length=10, unique=True)
    gender                  = models.CharField(max_length=8, choices=SEX)
    dob                     = models.DateField(verbose_name='Date of Birth')
    form                    = models.CharField(max_length=7, choices=FORMS)
    stream                  = models.CharField(max_length=1, choices=STREAMS)
    joined_school_at        = models.DateField(verbose_name="Started on", blank=True, null=True)
    updated_at              = models.DateTimeField(auto_now_add=True)
    profile_picture         = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    
    subject                 = models.ManyToManyField(Subject)

    # Guardian Info
    guardian_name           = models.CharField(max_length=30)
    guardian_phone          = models.CharField(max_length=12)
    guardian_email          = models.EmailField(unique=True)
    address                 = models.CharField(max_length=50)


    @property
    def age(self):
        today = date.today()
        dob   = self.dob

        age = today.year - dob.year

        if (today.day, today.month) < (dob.day, dob.month):
            age -= 1

        return age
    

    @property
    def full_name(self):
        return f"{self.user.first_name} {self.user.last_name}"


    def __str__(self):
        return self.full_name


class SecretCodeNumber(models.Model):
    code  = models.PositiveIntegerField(validators=[MinValueValidator(1000)])

    def __str__(self):
        return f"{self.code}"


class Teacher(models.Model):
    user             = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    gender           = models.CharField(max_length=8, choices=SEX)
    marital_status   = models.CharField(max_length=8, choices=MARITAL_STATUS, blank=True, null=True)
    phone            = models.CharField(max_length=12)
    joined_at        = models.DateField(verbose_name="Joined on", blank=True, null=True)
    experience       = models.PositiveIntegerField(verbose_name='Years Of Experience', validators=[MinValueValidator(0)], blank=True, null=True)
    office           = models.CharField(max_length=80, verbose_name='Office', blank=True, null=True)
    profile_picture  = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    teachers_code    = models.CharField(verbose_name='Teachers Secret Code', max_length=8, blank=True, null=False)

    form_teacher     = models.CharField(verbose_name="Form Teacher", max_length=7, null=True, blank=True, choices=FORMS)
    ft_stream        = models.CharField(max_length=1, blank=True, choices=STREAMS)
    form_assigned    = models.CharField(max_length=7, blank=True, choices=FORMS)
    stream1          = models.CharField(max_length=1, choices=STREAMS, blank=True, null=True)
    form_assigned2   = models.CharField(max_length=7, choices=FORMS, blank=True, null=True)
    stream2          = models.CharField(max_length=1, choices=STREAMS, blank=True, null=True)
    form_assigned3   = models.CharField(max_length=7, choices=FORMS, blank=True, null=True)
    stream3          = models.CharField(max_length=1, choices=STREAMS, blank=True, null=True)
    
    bio              = models.TextField(blank=True, null=True)

    subject          = models.ManyToManyField(Subject)


    @property
    def full_name(self):
        return f"{self.user.first_name} {self.user.last_name}"

    @property
    def status(self):
        if self.gender == 'male':
            status = 'Mr.'
        elif self.marital_status == 'Single' and self.gender  == 'female':
            status = 'Miss'
        elif self.marital_status == 'Married' and self.gender == 'female':
            status = 'Mrs.'

        return status


    @property
    def my_assigned_forms(self):
        pairs = [
            (f'{self.form_assigned}', f'{self.stream1}'), 
            (f'{self.form_assigned2}', f'{self.stream2}'), 
            (f'{self.form_assigned3}', f'{self.stream3}'), 
        ]

        return [(f, s) for f, s in pairs if f and s]


    @property
    def current_students(self):
        combos = [
            (self.form_assigned, self.stream1),
            (self.form_assigned2, self.stream2),
            (self.form_assigned3, self.stream3),
        ]

        students = Student.objects.none()

        for form, stream in combos:
            if form and stream:
                students |= Student.objects.filter(form=form, stream=stream)

        return students

    @property
    def student_class_counts(self):
        return self.current_students.values(
            'form', 'stream'
        ).annotate(
            count=Count('id')
        )

    @property
    def number_of_students(self):
        students = self.current_students
        total = 0

        for i in range(len(students)):
            total += 1

        return total



    @property
    def number_of_classes(self):
        combos = [
            (self.form_assigned, self.stream1),
            (self.form_assigned2, self.stream2),
            (self.form_assigned3, self.stream3),
        ]

        total = 0
        for form, stream in combos:
            if form and stream:
                total += 1

        return total



    def __str__(self):
        return self.user.email


class TeacherCode(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE, null=True)
    secret_code = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.secret_code}, for {self.user}"


class Grade(models.Model):
    student         = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='grades')
    subject         = models.ForeignKey(Subject, on_delete=models.CASCADE, null=True)
    ca1             = models.PositiveIntegerField(null=True, blank=True)
    ca2             = models.PositiveIntegerField(null=True, blank=True)
    et              = models.PositiveIntegerField(null=True, blank=True)
    ca1_out_of      = models.PositiveIntegerField(default=40, blank=True)
    ca2_out_of      = models.PositiveIntegerField(default=40, blank=True)
    et_out_of       = models.PositiveIntegerField(default=100, blank=True)
    remark          = models.TextField(max_length=100, null=True, blank=True)
    created_at      = models.DateTimeField(auto_now_add=True, null=True)

    @property
    def total_marks(self):
        ca1 = self.ca1
        ca2 = self.ca2
        et  = self.et

        ca1_out_of  = self.ca1_out_of
        ca2_out_of  = self.ca2_out_of
        et_out_of   = self.et_out_of
        
        # convert all student marks per grade from given max percentage to required percentage
        new_ca1 = (ca1/ca1_out_of) * 20
        new_ca2 = (ca2/ca2_out_of) * 20
        new_et = (et/et_out_of) * 60

        return round(new_ca1 + new_ca2 + new_et)

    @property
    def cont_assessment1_to_20 (self):
        return round((self.ca1/self.ca1_out_of) * 20)

    @property
    def cont_assessment2_to_20 (self):
        return round((self.ca2/self.ca2_out_of) * 20)

    @property
    def et_to_60 (self):
        return round((self.et/self.et_out_of) * 60)


    @property
    def grade(self):
        total_marks = self.total_marks

        if total_marks >= 80 and total_marks <= 100:
            grd = '1'
        elif total_marks >= 70 and total_marks <= 79:
            grd = 2
        elif total_marks >=65 and total_marks <= 69:
            grd = '3'
        elif total_marks >=60 and total_marks <= 64:
            grd = '4'
        elif total_marks >=55 and total_marks <= 59:
            grd = '5'
        elif total_marks >=50 and total_marks <= 54:
            grd = '6'
        elif total_marks >=45 and total_marks <= 49:
            grd = '7'
        elif total_marks >=40 and total_marks <= 44:
            grd =  '8'
        else:
            grd = '9'

        return grd

    def __str__(self):
        return f"Grades for {self.student.full_name}"

    class Meta:
        unique_together = ('student', 'subject')
    