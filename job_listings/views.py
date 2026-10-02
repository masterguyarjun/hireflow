from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Job, Category, Skill
from .forms import JobForm
from user_accounts.models import EmployerProfile


def job_list_view(request):
    jobs = Job.objects.filter(status='published').select_related('employer__user', 'category').prefetch_related('skills')

    # Search functionality
    query = request.GET.get('q')
    if query:
        jobs = jobs.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(employer__company_name__icontains=query) |
            Q(location__icontains=query) |
            Q(skills__name__icontains=query) |
            Q(category__name__icontains=query)
        ).distinct()

    # Filter functionality
    location_filter = request.GET.get('location')
    if location_filter:
        jobs = jobs.filter(location__icontains=location_filter)

    remote_filter = request.GET.get('remote')
    if remote_filter:
        jobs = jobs.filter(remote_option=remote_filter)

    employment_type_filter = request.GET.get('employment_type')
    if employment_type_filter:
        jobs = jobs.filter(employment_type=employment_type_filter)

    experience_level_filter = request.GET.get('experience_level')
    if experience_level_filter:
        jobs = jobs.filter(experience_level=experience_level_filter)

    category_filter = request.GET.get('category')
    if category_filter:
        jobs = jobs.filter(category__name=category_filter)

    # Salary range filtering
    salary_min = request.GET.get('salary_min')
    salary_max = request.GET.get('salary_max')
    if salary_min:
        try:
            jobs = jobs.filter(salary_min__gte=float(salary_min))
        except ValueError:
            pass
    if salary_max:
        try:
            jobs = jobs.filter(salary_max__lte=float(salary_max))
        except ValueError:
            pass

    # Skills filtering
    skills_filter = request.GET.get('skills')
    if skills_filter:
        skills_list = [s.strip() for s in skills_filter.split(',')]
        for skill in skills_list:
            jobs = jobs.filter(skills__name__icontains=skill)

    # Date posted filtering
    date_posted = request.GET.get('date_posted')
    if date_posted:
        from datetime import datetime, timedelta
        days_ago = int(date_posted)
        if days_ago > 0:
            date_threshold = datetime.now() - timedelta(days=days_ago)
            jobs = jobs.filter(created_at__gte=date_threshold)

    # Sorting
    sort_by = request.GET.get('sort', '-created_at')  # Default to newest first
    if sort_by == 'salary_low_high':
        jobs = jobs.order_by('salary_min')
    elif sort_by == 'salary_high_low':
        jobs = jobs.order_by('-salary_max')
    elif sort_by == 'oldest':
        jobs = jobs.order_by('created_at')
    else:  # newest (default)
        jobs = jobs.order_by('-created_at')

    # Pagination
    paginator = Paginator(jobs, 10)  # Show 10 jobs per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Get filter options for sidebar
    categories = Category.objects.all()
    skills = Skill.objects.all()[:20]  # Limit for performance

    context = {
        'page_obj': page_obj,
        'categories': categories,
        'skills': skills,
        'current_filters': {
            'q': query,
            'location': location_filter,
            'remote': remote_filter,
            'employment_type': employment_type_filter,
            'experience_level': experience_level_filter,
            'category': category_filter,
            'salary_min': salary_min,
            'salary_max': salary_max,
            'skills': skills_filter,
            'date_posted': date_posted,
            'sort': sort_by,
        }
    }
    return render(request, 'jobs/job_list.html', context)


def job_detail_view(request, slug):
    job = get_object_or_404(Job.objects.select_related('employer__user', 'category').prefetch_related('skills'), slug=slug, status='published')

    # Check if user has already applied
    has_applied = False
    if request.user.is_authenticated:
        from job_applications.models import Application
        has_applied = Application.objects.filter(job=job, applicant=request.user).exists()

    context = {
        'job': job,
        'has_applied': has_applied,
    }
    return render(request, 'jobs/job_detail.html', context)


@login_required
def job_create_view(request):
    # Check if user is an employer
    if not request.user.is_employer:
        messages.error(request, "Only employers can create job postings.")
        return redirect('user_dashboard:home')

    try:
        employer_profile = request.user.employer_profile
    except EmployerProfile.DoesNotExist:
        messages.error(request, "Please complete your employer profile first.")
        return redirect('user_accounts:edit_profile')

    if request.method == 'POST':
        form = JobForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.employer = employer_profile
            job.save()
            form.save_multiple()  # For many-to-many fields

            if 'publish' in request.POST:
                job.status = 'published'
                from django.utils import timezone
                job.published_at = timezone.now()
                job.save()
                messages.success(request, "Job published successfully!")
            else:
                messages.success(request, "Job saved as draft!")

            return redirect('job_listings:job_detail', slug=job.slug)
    else:
        form = JobForm()

    return render(request, 'jobs/job_form.html', {'form': form, 'title': 'Create Job'})


@login_required
def job_edit_view(request, slug):
    job = get_object_or_404(Job, slug=slug)

    # Check if user is the employer of this job
    if not request.user.is_employer or job.employer.user != request.user:
        messages.error(request, "You don't have permission to edit this job.")
        return redirect('user_dashboard:home')

    if request.method == 'POST':
        form = JobForm(request.POST, instance=job)
        if form.is_valid():
            job = form.save(commit=False)
            job.save()
            form.save_multiple()  # For many-to-many fields

            if 'publish' in request.POST:
                job.status = 'published'
                from django.utils import timezone
                job.published_at = timezone.now()
                job.save()
                messages.success(request, "Job published successfully!")
            else:
                messages.success(request, "Job updated successfully!")

            return redirect('job_listings:job_detail', slug=job.slug)
    else:
        form = JobForm(instance=job)

    return render(request, 'jobs/job_form.html', {'form': form, 'title': 'Edit Job', 'job': job})


@login_required
def job_delete_view(request, slug):
    job = get_object_or_404(Job, slug=slug)

    # Check if user is the employer of this job
    if not request.user.is_employer or job.employer.user != request.user:
        messages.error(request, "You don't have permission to delete this job.")
        return redirect('user_dashboard:home')

    if request.method == 'POST':
        job_title = job.title
        job.delete()
        messages.success(request, f"Job '{job_title}' deleted successfully.")
        return redirect('user_dashboard:dashboard')

    return render(request, 'jobs/job_confirm_delete.html', {'job': job})


@login_required
def job_publish_view(request, slug):
    job = get_object_or_404(Job, slug=slug)

    # Check if user is the employer of this job
    if not request.user.is_employer or job.employer.user != request.user:
        messages.error(request, "You don't have permission to publish this job.")
        return redirect('user_dashboard:home')

    job.status = 'published'
    from django.utils import timezone
    job.published_at = timezone.now()
    job.save()
    messages.success(request, "Job published successfully!")
    return redirect('job_listings:job_detail', slug=job.slug)


@login_required
def job_close_view(request, slug):
    job = get_object_or_404(Job, slug=slug)

    # Check if user is the employer of this job
    if not request.user.is_employer or job.employer.user != request.user:
        messages.error(request, "You don't have permission to close this job.")
        return redirect('user_dashboard:home')

    job.status = 'closed'
    job.save()
    messages.success(request, "Job closed successfully.")
    return redirect('job_listings:job_detail', slug=job.slug)