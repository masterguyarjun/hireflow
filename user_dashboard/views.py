from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Count, Q
from .models import SavedJob
from job_listings.models import Job
from job_applications.models import Application
from user_accounts.models import JobSeekerProfile, EmployerProfile


def home_view(request):
    # Show featured jobs and statistics
    featured_jobs = Job.objects.filter(
        status='published',
        featured=True
    ).select_related('employer__user', 'category').prefetch_related('skills')[:6]

    recent_jobs = Job.objects.filter(
        status='published'
    ).select_related('employer__user', 'category').prefetch_related('skills').order_by('-created_at')[:6]

    # Statistics
    stats = {
        'total_jobs': Job.objects.filter(status='published').count(),
        'total_companies': Job.objects.values('employer').distinct().count(),
        'total_applications': Application.objects.count(),
    }

    context = {
        'featured_jobs': featured_jobs,
        'recent_jobs': recent_jobs,
        'stats': stats,
    }
    return render(request, 'dashboard/home.html', context)


@login_required
def dashboard_view(request):
    if request.user.is_job_seeker:
        return job_seeker_dashboard(request)
    elif request.user.is_employer:
        return employer_dashboard(request)
    elif request.user.is_admin:
        return admin_dashboard(request)
    else:
        return redirect('dashboard:home')


def job_seeker_dashboard(request):
    if not request.user.is_job_seeker:
        messages.error(request, "Access denied.")
        return redirect('dashboard:home')

    # Get seeker's applications
    applications = Application.objects.filter(
        applicant=request.user
    ).select_related('job', 'job__employer__user').order_by('-applied_at')

    # Get seeker's saved jobs
    saved_jobs = SavedJob.objects.filter(
        user=request.user
    ).select_related('job', 'job__employer__user', 'job__category').prefetch_related('job__skills')

    # Application statistics
    app_stats = applications.values('status').annotate(count=Count('status'))
    app_stats_dict = {item['status']: item['count'] for item in app_stats}

    context = {
        'applications': applications[:5],  # Recent 5 applications
        'saved_jobs': saved_jobs[:5],  # Recent 5 saved jobs
        'app_stats': app_stats_dict,
        'total_applications': applications.count(),
    }
    return render(request, 'dashboard/job_seeker_dashboard.html', context)


def employer_dashboard(request):
    if not request.user.is_employer:
        messages.error(request, "Access denied.")
        return redirect('dashboard:home')

    try:
        employer_profile = request.user.employer_profile
    except EmployerProfile.DoesNotExist:
        messages.error(request, "Please complete your employer profile first.")
        return redirect('user_accounts:edit_profile')

    # Get employer's jobs
    jobs = Job.objects.filter(employer=employer_profile).order_by('-created_at')

    # Get recent applications for employer's jobs
    recent_applications = Application.objects.filter(
        job__employer=employer_profile
    ).select_related('job', 'applicant').order_by('-applied_at')[:10]

    # Job statistics
    job_stats = jobs.values('status').annotate(count=Count('status'))
    job_stats_dict = {item['status']: item['count'] for item in job_stats}

    # Application statistics for employer's jobs
    apps_for_jobs = Application.objects.filter(job__employer=employer_profile)
    app_stats = apps_for_jobs.values('status').annotate(count=Count('status'))
    app_stats_dict = {item['status']: item['count'] for item in app_stats}

    context = {
        'jobs': jobs,
        'recent_applications': recent_applications,
        'job_stats': job_stats_dict,
        'app_stats': app_stats_dict,
        'total_jobs': jobs.count(),
        'total_applications': apps_for_jobs.count(),
    }
    return render(request, 'dashboard/employer_dashboard.html', context)


def admin_dashboard(request):
    if not request.user.is_admin:
        messages.error(request, "Access denied.")
        return redirect('dashboard:home')

    # Admin statistics
    from user_accounts.models import User
    stats = {
        'total_users': User.objects.count(),
        'job_seekers': User.objects.filter(account_type='job_seeker').count(),
        'employers': User.objects.filter(account_type='employer').count(),
        'admins': User.objects.filter(account_type='admin').count(),
        'total_jobs': Job.objects.count(),
        'published_jobs': Job.objects.filter(status='published').count(),
        'total_applications': Application.objects.count(),
    }

    # Recent activity
    recent_users = User.objects.order_by('-date_joined')[:5]
    recent_jobs = Job.objects.order_by('-created_at')[:5]
    recent_applications = Application.objects.order_by('-applied_at')[:5]

    context = {
        'stats': stats,
        'recent_users': recent_users,
        'recent_jobs': recent_jobs,
        'recent_applications': recent_applications,
    }
    return render(request, 'dashboard/admin_dashboard.html', context)


@login_required
def saved_jobs_view(request):
    if not request.user.is_job_seeker:
        messages.error(request, "Only job seekers can view saved jobs.")
        return redirect('dashboard:home')

    saved_jobs = SavedJob.objects.filter(
        user=request.user
    ).select_related('job', 'job__employer__user', 'job__category').prefetch_related('job__skills')

    context = {
        'saved_jobs': saved_jobs,
    }
    return render(request, 'dashboard/saved_jobs.html', context)


@login_required
def save_job_view(request, job_slug):
    if not request.user.is_job_seeker:
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'success': False, 'error': 'Only job seekers can save jobs'}, status=403)
        messages.error(request, "Only job seekers can save jobs.")
        return redirect('job_listings:job_detail', slug=job_slug)

    job = get_object_or_404(Job, slug=job_slug, status='published')

    saved_job, created = SavedJob.objects.get_or_create(user=request.user, job=job)
    if created:
        message = "Job saved successfully!"
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'success': True, 'message': message, 'saved': True})
        messages.success(request, message)
    else:
        message = "Job is already saved."
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'success': True, 'message': message, 'saved': True})
        messages.info(request, message)

    return redirect('job_listings:job_detail', slug=job_slug)


@login_required
def unsave_job_view(request, job_slug):
    if not request.user.is_job_seeker:
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'success': False, 'error': 'Only job seekers can unsave jobs'}, status=403)
        messages.error(request, "Only job seekers can unsave jobs.")
        return redirect('job_listings:job_detail', slug=job_slug)

    job = get_object_or_404(Job, slug=job_slug)
    try:
        saved_job = SavedJob.objects.get(user=request.user, job=job)
        saved_job.delete()
        message = "Job removed from saved jobs."
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'success': True, 'message': message, 'saved': False})
        messages.success(request, message)
    except SavedJob.DoesNotExist:
        message = "Job is not in your saved jobs."
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'success': True, 'message': message, 'saved': False})
        messages.info(request, message)

    return redirect('job_listings:job_detail', slug=job_slug)