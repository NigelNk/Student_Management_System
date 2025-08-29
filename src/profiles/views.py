from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied, ValidationError
from django.contrib import messages
from django.views import View
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST,require_GET,require_http_methods

from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.shortcuts import redirect
from django.views.generic.edit import UpdateView, CreateView
from django.views.generic import ListView, TemplateView, DetailView

from .forms import StudentForm, TeacherForm, SubjectForm
from .models import Student, Teacher, Subject, Grade, TeacherCode, SecretCodeNumber


def profile_redirect_view(request):
    user = request.user
    if not user.is_authenticated:
        return redirect('login')

    if user.role == 'student':
        student = Student.objects.get(user=user)
        return redirect('student_update', pk=student.pk)
    elif user.role == 'teacher':
        teacher = Teacher.objects.get(user=user)
        return redirect('teacher_update', pk=teacher.pk)
    else:
        raise PermissionDenied("Invalid user role.")


def profile_create_redirect_view(request):
    user = request.user
    if not user.is_authenticated:
        return redirect('login')

    if user.role == 'student':
        return redirect('student_create')
    elif user.role == 'teacher':

        return redirect('teacher_create')
    else:
        raise PermissionDenied("Invalid user role.")


@login_required
def refresh_subjects(request):
    student = request.user.student

    form_map = {
        'Form 1': 1,
        'Form 2': 2,
        'Form 3': 3,
        'Form 4': 4
    }

    form_number = form_map.get(student.form)
    if form_number:
        all_subjects = Subject.objects.filter(subject_form=form_number)
        student.subject.set(all_subjects)

    return redirect('subjects')

@login_required
def update_profile_picture(request):

    if request.method == 'POST' and request.FILES.get('profile_picture'):
        student = request.user.student
        student.profile_picture = request.FILES['profile_picture']
        student.save()
        messages.success(request, "Your profile picture has been updated successfully!")


    return redirect('student_account_manager', pk=student.pk)


class StudentSubjectView(LoginRequiredMixin, ListView):
	model  				= Subject
	template_name 		= 'profiles/students/student_subjects.html'
	context_object_name = 'subjects'
	login_url			= 'login'


class StudentDetailView(LoginRequiredMixin, DetailView):
	model 				= Student
	template_name		= 'profiles/students/student_account.html'
	context_object_name	= 'student'
	login_url			= 'login'


	def dispatch(self, request, *args, **kwargs):
		if not Student.objects.filter(user=request.user).exists():
			return redirect('student_create')
		return super().dispatch(request, *args, **kwargs)


class StudentGradesView(LoginRequiredMixin, TemplateView):
	template_name 		= 'profiles/students/student_see_grades.html'
	login_url			= 'login'
	

class StudentCreationFormView(LoginRequiredMixin, CreateView):
	model 				= Student
	form_class 			= StudentForm
	success_url 		= reverse_lazy('home')
	template_name 		= 'profiles/create_profile.html'
	login_url			= 'login'


	def dispatch(self, request, *args, **kwargs):
		if Student.objects.filter(user=request.user).exists():
			messages.warning(request, "You have already submitted your student Info")
			return redirect('home')
		return super().dispatch(request, *args, **kwargs)


	def form_valid(self, form):
		form.instance.user = self.request.user
		
		student = form.save(commit=False)
		student.student_id = 'KT-MZU-00' + str(form.instance.user.pk) + '-2025'

		student.save()

		form_map = {
			'Form 1':1,
			'Form 2':2,
			'Form 3':3,
			'Form 4':4,
		}
		form_number = form_map.get(student.form)
		if form_number:
			all_subjects = Subject.objects.filter(subject_form=form_number)
			student.subject.set(all_subjects)

		for subject in student.subject.all():
			Grade.objects.create(student=self.request.user.student, subject=subject, ca1=0, ca2=0, et=0, grade='-', remark='-')


		return super().form_valid(form)


class TeacherCreationFormView(LoginRequiredMixin, CreateView):
	model 			= Teacher
	form_class 		= TeacherForm
	success_url 	= reverse_lazy('home')
	template_name 	= 'profiles/create_profile.html'
	login_url		= 'login'


	def dispatch(self, request, *args, **kwargs):
		if Teacher.objects.filter(user=request.user).exists():
			messages.warning(request, "You already have already submitted your staff Info")
			return redirect('home')
		return super().dispatch(request, *args, **kwargs)


	def form_valid(self, form):
		form.instance.user = self.request.user

		teacher = form.save(commit=False)

		initial = teacher.user.first_name[0].upper()

		code_obj = SecretCodeNumber.objects.get(id=1)
		# generate a secret code 
		secret_code = initial + str(code_obj.code)
		# get the submitted code
		submitted_code = form.cleaned_data.get('teachers_code')

		if submitted_code == secret_code:
			teacher.teachers_code = secret_code
			TeacherCode.objects.create(user=self.request.user, secret_code=secret_code)

			teacher.save()
			form.save_m2m()

			return super().form_valid(form)


		else:
			form.add_error('teachers_code', '❌ Invalid secret code.')
			return self.form_invalid(form)

		
		

# class StudentUpdateView(LoginRequiredMixin, UpdateView):
# 	model			= Student
# 	fields			= ['student_id', 'gender', 'dob', 'form', 'stream', 'joined_school_at', 'guardian_name', 'guardian_phone', 'guardian_email']
# 	template_name 	= 'profiles/update_profile.html'
# 	success_url 	= reverse_lazy('home')
# 	login_url		= 'login'


# 	def get_object(self, queryset=None):
# 		obj = super().get_object(queryset)
# 		if obj.user != self.request.user:
# 		    raise PermissionDenied()
# 		return obj


class TeacherUpdateView(LoginRequiredMixin, UpdateView):
	model			= Teacher
	fields			= '__all__'
	template_name 	= 'profiles/update_profile.html'
	success_url 	= reverse_lazy('home')
	login_url		= 'login'


	def get_object(self, queryset=None):
		obj = super().get_object(queryset)
		if obj.user != self.request.user:
		    raise PermissionDenied()
		return obj


class StudentRecordView(TemplateView):
	template_name = 'profiles/teachers/student_records.html'



class StudentFormTeacherView(LoginRequiredMixin, ListView):
	model 				= Student
	template_name 		= 'profiles/students/teacher_profiles.html'
	login_url			= 'login'
	context_object_name = 'students'


	def get_context_data(self, *args, **kwargs):
		context = super().get_context_data(*args, **kwargs)

		student = self.request.user.student
		target_pairs = (student.form, student.stream)

		matching_teachers = [
			teacher for teacher in Teacher.objects.all()
			if target_pairs in teacher.my_assigned_forms
		]

		context['teachers'] = matching_teachers

		return context



def dashboard_view(request):
    # Simulated data - fetch from your actual models
    class_names = ["Form 1A", "Form 1B"]
    boys_data = [6, 8]
    girls_data = [12, 9]

    context = {
        'total_groups': 20,
        'total_members': 123,
        'class_names': class_names,
        'boys_data': boys_data,
        'girls_data': girls_data,
    }
    return render(request, 'profiles/teachers/groups.html', context)


def enter_student_grades_view(request, student_id):
    student = get_object_or_404(Student, student_id=student_id)
    subject_id = request.GET.get('subject_id')  # Get selected subject from query string

    students = list(Student.objects.order_by('id'))

    current_index = students.index(student)
    
    previous_student = students[current_index - 1] if current_index > 0 else None
    next_student = students[current_index + 1] if current_index < len(students) - 1 else None


    selected_subject = None
    grades = None

    if subject_id:
        try:
            selected_subject = Subject.objects.get(id=subject_id)
            grades = Grade.objects.filter(student=student, subject=selected_subject).first()
        except Subject.DoesNotExist:
            selected_subject = None
            grades = None

    context = {
        'student': student,
        'selected_subject': selected_subject,
        'grades': grades,
        'previous_student': previous_student,
	    'next_student': next_student,

    }

    return render(request, 'profiles/teachers/enter_student_grades.html', context)


@login_required
def manage_student_grades(request, student_id):
    student = get_object_or_404(Student, pk=student_id)
    students = list(Student.objects.order_by('id'))

    current_index = students.index(student)
    previous_student = students[current_index - 1] if current_index > 0 else None
    next_student = students[current_index + 1] if current_index < len(students) - 1 else None

    # Get subject_id from the query string
    subject_id = request.GET.get('subject_id')
    selected_subject = None
    grades = None

    if subject_id:
        try:
            selected_subject = Subject.objects.get(id=subject_id)
            grades = Grade.objects.filter(student=student, subject=selected_subject).first()
        except Subject.DoesNotExist:
            selected_subject = None

    context = {
        'student': student,
        'previous_student': previous_student,
        'next_student': next_student,
        'selected_subject': selected_subject,
        'grades': grades,
    }

    return render(request, 'profiles/teachers/enter_student_grades.html', context)


@login_required
def update_students_grade(request, student_id):
    student = get_object_or_404(Student, student_id=student_id)

    if request.method == 'POST':
        subject_id 	= request.POST.get('subject')
        ca1 		= request.POST.get('ca1') or 0
        ca2 		= request.POST.get('ca2') or 0
        et 			= request.POST.get('et') or 0
        

        c1_max_marks = request.POST.get('ca1_out_of')
        c2_max_marks = request.POST.get('ca2_out_of')
        et_max_marks = request.POST.get('et_out_of')
        remark 		= request.POST.get('remark')

        if not subject_id:
            messages.error(request, "Subject is required.")
            return redirect('enter_grades', student_id=student_id)

        subject = get_object_or_404(Subject, id=subject_id)

        # Get or create grade record
        grade_obj, created = Grade.objects.get_or_create(
            student=student,
            subject=subject,
            defaults={
                'ca1': ca1,
                'ca2': ca2,
                'et': et,
                'ca1_out_of': c1_max_marks,
                'ca2_out_of': c2_max_marks,
                'et_out_of': et_max_marks,
                'remark': remark,
            }
        )

        if not created:
            # Update existing record
            grade_obj.ca1 = ca1
            grade_obj.ca2 = ca2
            grade_obj.et = et
            grade_obj.ca1_out_of = c1_max_marks
            grade_obj.ca2_out_of = c2_max_marks
            grade_obj.et_out_of = et_max_marks
            grade_obj.remark = remark
            grade_obj.save()

        messages.success(request, "Grade updated successfully.")
        return redirect(f"{reverse('enter_grades', args=[student_id])}?subject_id={subject_id}")


    # If not POST, redirect to grade entry page
    return redirect('enter_grades', student_id=student_id)

@login_required
def see_student_details(request, student_id):
	student = get_object_or_404(Student, student_id=student_id)
	return render(request, 'profiles/teachers/openModal.html', {'student': student})


@login_required
def teacher_account_view(request):
    teacher = Teacher.objects.get(user=request.user)
    return render(request, 'profiles/teachers/teacher_account.html', {'teacher': teacher})
	

@login_required
@csrf_protect
def choose_subject(request, student_id):
    student = get_object_or_404(Student, student_id=student_id)
    grades = None
    selected_subject = None
    subject_id = None

    # rebuild the student list for previous/next navigation
    students = list(Student.objects.order_by('id'))

    try:
        current_index = students.index(student)
        previous_student = students[current_index - 1] if current_index > 0 else None
        next_student = students[current_index + 1] if current_index < len(students) - 1 else None
    except ValueError:
        previous_student = None
        next_student = None

    # Handle subject selection
    if request.method == 'POST':
        subject_id = request.POST.get('subject')
        if subject_id:
            selected_subject = get_object_or_404(Subject, id=subject_id)
            grades = Grade.objects.filter(student=student, subject=selected_subject).first()

    context = {
        'student': student,
        'grades': grades,
        'selected_subject': selected_subject,
        'previous_student': previous_student,
        'next_student': next_student,
    }

    return redirect(f"{reverse('enter_grades', args=[student_id])}?subject_id={subject_id}")


