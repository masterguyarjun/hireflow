from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from .models import Application
from job_listings.models import Job
from .forms import ApplicationForm
from user_accounts.models import JobSeekerProfile


@login_required
def apply_for_job_view(request, job_slug):
    job = get_object_or_404(Job, slug=job_slug, status='published')

    # Check if user is a job seeker
    if not request.user.is_job_seeker:
        messages.error(request, "Only job seekers can apply for jobs.")
        return redirect('job_listings:job_detail', slug=job_slug)

    # Check if user already applied
    if Application.objects.filter(job=job, applicant=request.user).exists():
        messages.warning(request, "You have already applied for this job.")
        return redirect('job_listings:job_detail', slug=job_slug)

    if request.method == 'POST':
        form = ApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            application = form.save(commit=False)
            application.job = job
            application.applicant = request.user
            application.save()

            messages.success(request, "Your application has been submitted successfully!")
            return redirect('job_applications:my_applications')
    else:
        form = ApplicationForm()

    return render(request, 'applications/apply.html', {
        'form': form,
        'job': job
    })


@login_required
def my_applications_view(request):
    # Check if user is a job seeker
    if not request.user.is_job_seeker:
        messages.error(request, "Only job seekers can view their applications.")
        return redirect('user_dashboard:home')

    applications = Application.objects.filter(applicant=request.user).select_related(
        'job', 'job__employer__user'
    ).order_by('-applied_at')

    # Filter by status if requested
    status_filter = request.GET.get('status')
    if status_filter:
        applications = applications.filter(status=status_filter)

    context = {
        'applications': applications,
        'status_filter': status_filter,
        'status_choices': Application.STATUS_CHOICES,
    }
    return render(request, 'applications/my_applications.html', context)


@login_required
def application_detail_view(request, application_id):
    application = get_object_or_404(Application, id=application_id)

    # Check permissions
    if request.user == application.applicant:
        # Job seeker viewing their own application
        template = 'applications/application_detail_seeker.html'
    elif request.user.is_employer and application.job.employer.user == request.user:
        # Employer viewing application for their job
        template = 'applications/application_detail_employer.html'
    else:
        messages.error(request, "You don't have permission to view this application.")
        return redirect('user_dashboard:home')

    return render(request, template, {'application': application})


@login_required
def update_application_status_view(request, application_id):
    application = get_object_or_404(Application, id=application_id)

    # Check if user is the employer of this job
    if not request.user.is_employer or application.job.employer.user != request.user:
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'success': False, 'error': 'Permission denied'}, status=403)
        messages.error(request, "You don't have permission to update this application.")
        return redirect('user_dashboard:home')

    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status in dict(Application.STATUS_CHOICES):
            application.status = new_status
            application.save()

            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'success': True, 'new_status': application.get_status_display()})

            messages.success(request, f"Application status updated to {application.get_status_display()}.")
            return redirect('job_applications:application_detail', application_id=application.id)
        else:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'success': False, 'error': 'Invalid status'}, status=400)
            messages.error(request, "Invalid status provided.")

    return redirect('job_applications:application_detail', application_id=application.id)