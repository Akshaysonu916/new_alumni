from django.contrib.auth.models import AbstractUser,Group,Permission
from django.db import models

class User(AbstractUser):
    is_alumni = models.BooleanField(default=False)
    is_student = models.BooleanField(default=False)

    groups = models.ManyToManyField(Group, related_name="custom_user_groups", blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name="custom_user_permissions", blank=True)

class AlumniProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="alumni_profile")
    profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
    bio = models.TextField(blank=True)
    company = models.CharField(max_length=255)
    job_title = models.CharField(max_length=255)
    graduation_year = models.IntegerField(null=True,blank=True)
    linkedin = models.URLField(blank=True, null=True)

    def _str_(self):
        return self.user.username

class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="student_profile")
    major = models.CharField(max_length=255)
    enrollment_year = models.IntegerField()
    resume = models.FileField(upload_to="resumes/", blank=True, null=True)

    def _str_(self):
        return self.user.username
    

class JobPost(models.Model):
    job_name = models.CharField(max_length=255)
    company = models.CharField(max_length=255)
    description = models.TextField()
    job_type = models.CharField(max_length=50)
    application_link = models.URLField()
    company_website = models.URLField()
    alumni = models.ForeignKey('AlumniProfile', on_delete=models.CASCADE, null=True, blank=True)  # Allow null

    def _str_(self):
        return self.job_name

class Photo(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to="photos/")
    upload_date = models.DateTimeField(auto_now_add=True)

    def _str_(self):
        return self.title