from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required,user_passes_test
from django.contrib import messages
from .models import *
from .forms import *

def signup_view(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('signin')  # Redirect to login after successful signup
    else:
        form = SignUpForm()  # Ensure 'form' is always defined

    return render(request, 'signup.html', {'form': form})

def signin_view(request):
    if request.method == 'POST':
        form = SignInForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                if hasattr(user, 'alumni_profile'):
                    return redirect('alumni_dashboard')
                elif hasattr(user, 'student_profile'):
                    return redirect('student_dashboard')
                elif user.is_staff:
                    return redirect('admin:index')
                else:
                    return redirect('home')
            else:
                messages.error(request, 'Invalid username or password')
    else:
        form = SignInForm()
    return render(request, 'signin.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('signin')

def home_view(request):
    return render(request, 'home.html', {'user': request.user})



# Helper function to check if user is alumni
def is_alumni(user):
    return user.is_authenticated and hasattr(user, 'alumni_profile')

# Alumni Dashboard
@login_required(login_url='signin')
@user_passes_test(is_alumni, login_url='home')
def alumni_dashboard(request):
    if not hasattr(request.user, 'alumni_profile'):
        messages.error(request, "You are not an alumni.")
        return redirect('home')

    alumni = request.user.alumni_profile
    return render(request, 'alumni/dashboard.html', {'alumni': alumni})

# Job Post Management for Alumni
@login_required(login_url='signin')
@user_passes_test(is_alumni, login_url='home')
def job_list(request):
    jobs = JobPost.objects.all()
    return render(request, 'alumni/job_list.html', {'jobs': jobs})

@login_required(login_url='signin')
@user_passes_test(is_alumni, login_url='home')
def add_job(request):
    if request.method == 'POST':
        form = JobPostForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Job post created successfully.')
            return redirect('job_list')
    else:
        form = JobPostForm()
    return render(request, 'alumni/add_job.html', {'form': form})

@login_required(login_url='signin')
@user_passes_test(is_alumni, login_url='home')
def edit_job(request, job_id):
    job = get_object_or_404(JobPost, id=job_id)
    if request.method == 'POST':
        form = JobPostForm(request.POST, instance=job)
        if form.is_valid():
            form.save()
            messages.success(request, 'Job post updated successfully.')
            return redirect('job_list')
    else:
        form = JobPostForm(instance=job)
    return render(request, 'alumni/edit_job.html', {'form': form, 'job': job})

@login_required(login_url='signin')
@user_passes_test(is_alumni, login_url='home')
def delete_job(request, job_id):
    job = get_object_or_404(JobPost, id=job_id)
    if request.method == 'POST':
        job.delete()
        messages.success(request, 'Job post deleted successfully.')
        return redirect('job_list')
    return render(request, 'alumni/delete_job.html', {'job': job})

# Gallery view for Alumni - Reusing shared gallery functionality
@login_required(login_url='signin')
@user_passes_test(is_alumni, login_url='home')
def alumni_gallery_view(request):
    photos = Photo.objects.all().order_by('-upload_date')
    return render(request, 'gallery/photo_gallery.html', {'photos': photos})


# Alumni Dashboard
@login_required(login_url='signin')
# @user_passes_test(is_alumni, login_url='home')
def alumni_dashboard(request):
    alumni = request.user.alumni_profile
    return render(request, 'dashboard.html', {'alumni': alumni})

# Job Post Management for Alumni
@login_required(login_url='signin')
@user_passes_test(is_alumni, login_url='home')
def job_list(request):
    jobs = JobPost.objects.all()
    return render(request, 'alumni/job_list.html', {'jobs': jobs})

@login_required(login_url='signin')
# @user_passes_test(is_alumni, login_url='home')
def add_job(request):
    if request.method == 'POST':
        form = JobPostForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.alumni = request.user.alumni_profile
            job.save()
            messages.success(request, 'Job post created successfully.')
            return redirect('job_list')
    else:
        form = JobPostForm()
    return render(request, 'add_job.html', {'form': form})

@login_required(login_url='signin')
@user_passes_test(is_alumni, login_url='home')
def edit_job(request, job_id):
    job = get_object_or_404(JobPost, id=job_id)
    if request.user.alumni_profile != job.alumni:
        messages.error(request, 'You are not authorized to edit this job.')
        return redirect('job_list')

    if request.method == 'POST':
        form = JobPostForm(request.POST, instance=job)
        if form.is_valid():
            form.save()
            messages.success(request, 'Job post updated successfully.')
            return redirect('job_list')
    else:
        form = JobPostForm(instance=job)
    return render(request, 'alumni/edit_job.html', {'form': form, 'job': job})

@login_required(login_url='signin')
@user_passes_test(is_alumni, login_url='home')
def delete_job(request, job_id):
    job = get_object_or_404(JobPost, id=job_id)
    if request.user.alumni_profile != job.alumni:
        messages.error(request, 'You are not authorized to delete this job.')
        return redirect('job_list')

    if request.method == 'POST':
        job.delete()
        messages.success(request, 'Job post deleted successfully.')
        return redirect('job_list')
    return render(request, 'alumni/delete_job.html', {'job': job})

# Gallery view for Alumni
@login_required(login_url='signin')
@user_passes_test(is_alumni, login_url='home')
def alumni_gallery_view(request):
    photos = Photo.objects.all().order_by('-upload_date')
    return render(request, 'gallery/photo_gallery.html', {'photos': photos})


@login_required
def profile_view(request):
    return render(request, 'profile.html')


@login_required
def edit_profile(request):
    # Corrected: Access 'alumni_profile' instead of 'profile'
    profile, created = AlumniProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = AlumniProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile')  # Redirect to profile page
    else:
        form = AlumniProfileForm(instance=profile)
    
    return render(request, 'edit_profile.html', {'form': form})