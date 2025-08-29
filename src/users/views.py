from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.urls import reverse_lazy, reverse
from django.views.generic.edit import UpdateView, CreateView

from .models import CustomUser
from .forms import CustomUserCreationForm, CustomUserChangeForm


class CustomUserCreationFormView(CreateView):
	form_class 		= CustomUserCreationForm
	success_url		= reverse_lazy('home')
	template_name 	= 'users/signup.html'


	def form_valid(self, form):
		user = form.save()
		login(self.request, user)
		return redirect(self.success_url)


class CustomUserUpdate(LoginRequiredMixin, UpdateView):
	model			= CustomUser
	form_class 		= CustomUserChangeForm
	template_name 	= 'users/student_update.html'
	login_url 		= 'login'

	def get_success_url(self):
		return reverse_lazy('update',  kwargs={'pk': self.request.user.pk})

	def form_valid(self, form):
		messages.success(self.request, "Your profile has been updated successfully!")
		return super().form_valid(form)


