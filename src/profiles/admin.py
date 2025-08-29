
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import (
    Student,
    Teacher,
    Subject,
    Grade,
    TeacherCode, 
    SecretCodeNumber,
)

from .forms import StudentForm, TeacherForm


class SubjectInline(admin.TabularInline):
    model = Subject


class StudentAdmin(admin.ModelAdmin):
    form   = StudentForm
    list_display = ['user', 'student_id', 'form', 'stream',]
    search_fields = ['student_id', 'user',]

    filter_horizontal = ('subject',)



class TeacherAdmin(admin.ModelAdmin):
    form = TeacherForm
    list_display = ['user', 'gender', 'phone', 'form_teacher', 'ft_stream']
    filter_horizontal = ('subject',)


class GradeAdmin(admin.ModelAdmin):
    model  = Grade
    list_display = [
        'student', 'subject', 'ca1', 'ca2', 'et', 'grade', 'remark',
    ]


admin.site.register(Student, StudentAdmin)
admin.site.register(Teacher, TeacherAdmin)
admin.site.register(Grade, GradeAdmin)
admin.site.register(Subject)
admin.site.register(TeacherCode)
admin.site.register(SecretCodeNumber)
