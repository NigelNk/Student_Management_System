from django.db import models
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import AbstractUser



class CustomUser(AbstractUser):
    ROLE_CHOICE = [
        ('student', 'Student'),
        ('teacher', 'Teacher'),
    ]
    role    = models.CharField(max_length=10, choices=ROLE_CHOICE)


    def get_profiles(self):
        try:
            if self.role == 'teacher':
                return self.teacher
            elif self.role == 'student':
                return self.student
            else:
                return None
        except ObjectDoesNotExist:
            return None

    def __str__(self):
        return f"{self.email}"
    
