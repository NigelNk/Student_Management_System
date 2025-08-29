from django.urls import path

from .views import CustomUserCreationFormView, CustomUserUpdate


urlpatterns = [
	path('signup/', CustomUserCreationFormView.as_view(), name='signup'),
	path('update/<int:pk>/', CustomUserUpdate.as_view(), name='update'),
]