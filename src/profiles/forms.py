from django import forms
from django.contrib.auth import get_user_model

from .models import Student, Teacher, Subject, TeacherCode, Grade
from users.models import CustomUser


User = get_user_model()


class SubjectForm(forms.ModelForm):

    class Meta:
        model = Subject
        fields = ['subject_name', ]


class StudentForm(forms.ModelForm):
    
    class Meta:
        model = Student
        fields = ['gender', 'dob', 'form', 'stream','joined_school_at', 'profile_picture', 'guardian_name', 'guardian_phone', 'guardian_email', 'address']


class TeacherForm(forms.ModelForm):
    subject = forms.ModelMultipleChoiceField(
        queryset=Subject.objects.all(),
        widget=forms.SelectMultiple(attrs={'class': 'form-select'}),
        required=False
    )

    class Meta:

        model = Teacher
        fields = ['gender', 'marital_status', 'phone', 'joined_at', 'experience', 'office',
            'teachers_code', 'profile_picture', 'form_teacher', 'ft_stream',
            'form_assigned', 'stream1', 'form_assigned2', 'stream2', 'form_assigned3', 'stream3',
            'bio', 'subject']

    def clean(self):
        cleaned_data = super().clean()
        form_teacher = cleaned_data.get('form_teacher')
        ft_stream = cleaned_data.get('ft_stream')

        if form_teacher and ft_stream:
            current_teacher_id = self.instance.pk

            conflict = Teacher.objects.filter(
                form_teacher=form_teacher,
                ft_stream=ft_stream
            ).exclude(pk=current_teacher_id).exists()

            if conflict:
                raise forms.ValidationError(f"Sorry, this class ({form_teacher}{ft_stream}) has already been assigned to another teacher.")


class GradeForm(forms.ModelForm):

    class Meta:
        model = Grade
        fields = ['subject', 'ca1', 'ca2', 'et',]
