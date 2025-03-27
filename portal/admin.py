from django.contrib import admin
from .models import User, AlumniProfile, StudentProfile, JobPost, Photo

admin.site.register(User)
admin.site.register(AlumniProfile)
admin.site.register(StudentProfile)
admin.site.register(JobPost)
admin.site.register(Photo)