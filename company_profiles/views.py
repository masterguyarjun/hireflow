from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from .models import Company
from job_listings.models import Job


def company_list_view(request):
    companies = Company.objects.select_related('employer_profile__user').all()

    # Search functionality
    query = request.GET.get('q')
    if query:
        companies = companies.filter(
            Q(employer_profile__company_name__icontains=query) |
            Q(employer_profile__industry__icontains=query) |
            Q(specialties__icontains=query) |
            Q(culture_description__icontains=query)
        )

    # Pagination
    paginator = Paginator(companies, 12)  # Show 12 companies per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'search_query': query,
    }
    return render(request, 'companies/company_list.html', context)


def company_detail_view(request, company_id):
    company = get_object_or_404(Company.objects.select_related('employer_profile__user'), id=company_id)

    # Get jobs from this company
    jobs = Job.objects.filter(
        employer=company.employer_profile,
        status='published'
    ).order_by('-created_at')[:6]  # Show recent jobs

    context = {
        'company': company,
        'jobs': jobs,
    }
    return render(request, 'companies/company_detail.html', context)