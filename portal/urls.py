from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('signup/', views.signup_view, name='signup'),
    path('signin/', views.signin_view, name='signin'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.alumni_dashboard, name='alumni_dashboard'),
    
    # Job Post Management URLs
    path('jobs/', views.job_list, name='job_list'),
    path('jobs/add/', views.add_job, name='add_job'),
    path('jobs/edit/<int:job_id>/', views.edit_job, name='edit_job'),
    path('jobs/delete/<int:job_id>/', views.delete_job, name='delete_job'),

    # Alumni Gallery
    path('gallery/', views.alumni_gallery_view, name='alumni_gallery_view'),
    path('profile/', views.profile_view, name='profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
]