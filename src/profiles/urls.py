from django.urls import path


from .views import (
# StudentUpdateView,
profile_create_redirect_view, 
TeacherUpdateView, 
profile_redirect_view,
StudentCreationFormView,
TeacherCreationFormView,
StudentSubjectView,
StudentGradesView,
StudentDetailView,
StudentRecordView,
refresh_subjects,
StudentFormTeacherView,
teacher_account_view,
enter_student_grades_view,
update_profile_picture,
choose_subject,
update_students_grade,
see_student_details,
manage_student_grades,
# create_group_view,
dashboard_view,
)

urlpatterns = [
    # redirecting the user based on role (Student/teacher) for updating/creating profile
	path('profile/update/', profile_redirect_view, name='profile_update'),
	path('profile/create/', profile_create_redirect_view, name='profile_create'),

    # path('student/<int:pk>/update/', StudentUpdateView.as_view(), name='student_update'),
    path('teacher/<int:pk>/update/', TeacherUpdateView.as_view(), name='teacher_update'),

    path('student/create/', StudentCreationFormView.as_view(), name='student_create'),
    path('teacher/create/', TeacherCreationFormView.as_view(), name='teacher_create'),

    # Student subject view url
    path('student/subjects/', StudentSubjectView.as_view(), name='subjects'),
    # student subjects refresh
    path('subjects/refresh/', refresh_subjects, name='refresh_subjects'),
    # Student update profile picture
    path('update-picture/', update_profile_picture, name='update_profile_picture'),
    # student grades
    path('student/grades/', StudentGradesView.as_view(), name='see_grades'),
    # student accounts
    path('student/account/<int:pk>/', StudentDetailView.as_view(), name='student_account_manager'),
    
    path('student/form_teacher/', StudentFormTeacherView.as_view(), name='form_teacher'),
    # student records view (for teachers)
    path('teacher/student_records/', StudentRecordView.as_view(), name='student_records'),
    path('teacher/account/', teacher_account_view, name='teacher_account'),

    path('teacher/student_grades/<str:student_id>/', enter_student_grades_view, name='enter_grades'),
    # path('teacher/student/<str:student_id>/grades/', get_student_grades, name='get_student_grades'),

    path('choose_subject/<str:student_id>/', choose_subject, name='choose_subject'), #choose subject to manage its grade for
    path('update_grades/<str:student_id>/', update_students_grade, name='update_students_grade'),
    
    path('student_details/<str:student_id>/', see_student_details, name='see_student_details'),
    path('grades/manage/<int:student_id>/', manage_student_grades, name='manage_student_grades'),
    path('dashboard/', dashboard_view, name='group_dashboard'),
    # path('create-group/', create_group_view, name='create_group'),

    ] 
