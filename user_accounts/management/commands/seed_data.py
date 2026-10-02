from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils import timezone
from user_accounts.models import JobSeekerProfile, EmployerProfile
from job_listings.models import Job, Category, Skill
from job_applications.models import Application
from company_profiles.models import Company
from user_dashboard.models import SavedJob
from django.utils.text import slugify
import random

User = get_user_model()

class Command(BaseCommand):
    help = 'Create seed data for the HireFlow job portal'

    def handle(self, *args, **options):
        self.stdout.write('Creating seed data...')

        # Create admin user
        admin_user, created = User.objects.get_or_create(
            username='admin',
            defaults={
                'email': 'admin@hireflow.com',
                'first_name': 'Admin',
                'last_name': 'User',
                'is_staff': True,
                'is_superuser': True,
            }
        )
        if created:
            admin_user.set_password('admin123')
            admin_user.account_type = 'admin'
            admin_user.save()
            self.stdout.write(f'Created admin user: {admin_user.username}')

        # Create job seeker users
        job_seeker_data = [
            {
                'username': 'johndoe',
                'email': 'john.doe@email.com',
                'first_name': 'John',
                'last_name': 'Doe',
            },
            {
                'username': 'janesmith',
                'email': 'jane.smith@email.com',
                'first_name': 'Jane',
                'last_name': 'Smith',
            },
            {
                'username': 'bobwilson',
                'email': 'bob.wilson@email.com',
                'first_name': 'Bob',
                'last_name': 'Wilson',
            }
        ]

        for data in job_seeker_data:
            user, created = User.objects.get_or_create(
                username=data['username'],
                defaults={
                    'email': data['email'],
                    'first_name': data['first_name'],
                    'last_name': data['last_name'],
                }
            )
            if created:
                user.set_password('password123')
                user.account_type = 'job_seeker'
                user.save()

                # Create job seeker profile
                JobSeekerProfile.objects.create(
                    user=user,
                    professional_headline=f"{data['first_name']}'s Professional Headline",
                    bio=f"This is the bio for {data['first_name']} {data['last_name']}. Experienced professional seeking new opportunities.",
                    skills='Python, Django, JavaScript, HTML, CSS',
                    years_of_experience=random.randint(1, 5),
                    education='Bachelor\'s Degree in Computer Science',
                    current_job_title='Software Developer',
                    location='New York, NY',
                )
                self.stdout.write(f'Created job seeker: {user.username}')

        # Create employer users
        employer_data = [
            {
                'username': 'techcorp',
                'email': 'hr@techcorp.com',
                'first_name': 'Tech',
                'last_name': 'Corp',
            },
            {
                'username': 'startupxyz',
                'email': 'contact@startupxyz.com',
                'first_name': 'Startup',
                'last_name': 'XYZ',
            },
            {
                'username': 'enterpriseinc',
                'email': 'jobs@enterpriseinc.com',
                'first_name': 'Enterprise',
                'last_name': 'Inc',
            }
        ]

        for data in employer_data:
            user, created = User.objects.get_or_create(
                username=data['username'],
                defaults={
                    'email': data['email'],
                    'first_name': data['first_name'],
                    'last_name': data['last_name'],
                }
            )
            if created:
                user.set_password('password123')
                user.account_type = 'employer'
                user.save()

                # Create employer profile
                EmployerProfile.objects.create(
                    user=user,
                    company_name=f"{data['first_name']} {data['last_name']} Company",
                    company_description=f"We are {data['first_name']} {data['last_name']}, a leading company in our industry.",
                    industry=random.choice(['Technology', 'Finance', 'Healthcare', 'Education', 'Marketing']),
                    company_website=f'https://{data["username"]}.com',
                    company_location=random.choice(['New York, NY', 'San Francisco, CA', 'Seattle, WA', 'Austin, TX', 'Boston, MA']),
                    company_size=random.choice(['11-50', '51-200', '201-500', '501-1000', '1000+']),
                    contact_email=data['email'],
                )
                self.stdout.write(f'Created employer: {user.username}')

        # Create categories
        categories_data = [
            {'name': 'Software Development', 'description': 'Jobs in software development and programming'},
            {'name': 'Data Science', 'description': 'Jobs in data analysis, machine learning, and AI'},
            {'name': 'Design & UX', 'description': 'Jobs in UI/UX design, graphic design, and product design'},
            {'name': 'Marketing', 'description': 'Jobs in digital marketing, content creation, and brand management'},
            {'name': 'Sales', 'description': 'Jobs in sales, business development, and account management'},
            {'name': 'Customer Support', 'description': 'Jobs in customer service, technical support, and client relations'},
        ]

        for cat_data in categories_data:
            category, created = Category.objects.get_or_create(
                name=cat_data['name'],
                defaults=cat_data
            )
            if created:
                self.stdout.write(f'Created category: {category.name}')

        # Create skills
        skills_data = [
            'Python', 'JavaScript', 'TypeScript', 'React', 'Vue.js', 'Angular',
            'Node.js', 'Django', 'Flask', 'FastAPI', 'Spring Boot', '.NET',
            'Java', 'C#', 'C++', 'Go', 'Rust', 'PHP', 'Laravel',
            'HTML', 'CSS', 'SASS', 'Bootstrap', 'Tailwind CSS',
            'MySQL', 'PostgreSQL', 'MongoDB', 'Redis', 'Elasticsearch',
            'AWS', 'Azure', 'Google Cloud', 'Docker', 'Kubernetes',
            'Git', 'Jenkins', 'CI/CD', 'REST API', 'GraphQL',
            'Machine Learning', 'Deep Learning', 'TensorFlow', 'PyTorch',
            'Data Analysis', 'Pandas', 'NumPy', 'SQL', 'NoSQL',
            'UI/UX Design', 'Figma', 'Adobe XD', 'Photoshop', 'Illustrator',
            'Project Management', 'Agile', 'Scrum', 'Jira', 'Trello',
            'Digital Marketing', 'SEO', 'SEM', 'Google Analytics',
            'Content Writing', 'Copywriting', 'Social Media Marketing',
        ]

        for skill_name in skills_data:
            skill, created = Skill.objects.get_or_create(name=skill_name)
            if created:
                self.stdout.write(f'Created skill: {skill.name}')

        # Create companies linked to employer profiles
        employer_users = list(User.objects.filter(account_type='employer'))
        companies_data = [
            {
                'company_name': 'TechCorp Solutions',
                'description': 'Leading software development company specializing in custom enterprise solutions.',
                'industry': 'Technology',
                'website': 'https://techcorpsolutions.com',
                'location': 'New York, NY',
                'size': '201-500',
            },
            {
                'company_name': 'DataDriven Inc',
                'description': 'Innovative data science and analytics company helping businesses make data-driven decisions.',
                'industry': 'Technology',
                'website': 'https://datadriveninc.com',
                'location': 'San Francisco, CA',
                'size': '51-200',
            },
            {
                'company_name': 'CreativeDesign Studio',
                'description': 'Award-winning design studio creating beautiful user experiences and brand identities.',
                'industry': 'Design',
                'website': 'https://creativedesignstudio.com',
                'location': 'Seattle, WA',
                'size': '11-50',
            },
            {
                'company_name': 'MarketPro Agency',
                'description': 'Full-service marketing agency driving growth through innovative campaigns.',
                'industry': 'Marketing',
                'website': 'https://marketproagency.com',
                'location': 'Austin, TX',
                'size': '101-200',
            },
            {
                'company_name': 'GlobalSales Partners',
                'description': 'International sales and business development firm connecting companies with global opportunities.',
                'industry': 'Sales',
                'website': 'https://globalsalespartners.com',
                'location': 'Boston, MA',
                'size': '501-1000',
            }
        ]

        for i, company_data in enumerate(companies_data):
            if i < len(employer_users):
                employer_user = employer_users[i]
                try:
                    employer_profile = EmployerProfile.objects.get(user=employer_user)
                    company, created = Company.objects.get_or_create(
                        employer_profile=employer_profile,
                        defaults={
                            'founded_year': 2020,
                            'headquarters': company_data['location'],
                            'specialties': company_data['description'],
                            'culture_description': f"Innovative {company_data['industry']} company focused on excellence and innovation.",
                            'is_verified': True,
                        }
                    )
                    if created:
                        # Update the employer profile with company-specific info
                        employer_profile.company_name = company_data['company_name']
                        employer_profile.company_website = company_data['website']
                        employer_profile.company_location = company_data['location']
                        employer_profile.company_size = company_data['size']
                        employer_profile.save()
                        self.stdout.write(f'Created company: {company_data["company_name"]} for {employer_user.username}')
                except EmployerProfile.DoesNotExist:
                    self.stdout.write(
                        self.style.WARNING(f'EmployerProfile not found for {employer_user.username}')
                    )

        # Create jobs
        job_seekers = list(User.objects.filter(account_type='job_seeker'))
        employers = list(User.objects.filter(account_type='employer'))
        categories = list(Category.objects.all())
        companies = list(Company.objects.all())

        if job_seekers and employers and categories and companies:
            job_titles = [
                'Senior Software Engineer',
                'Full Stack Developer',
                'Frontend Developer',
                'Backend Developer',
                'Data Scientist',
                'Machine Learning Engineer',
                'UX/UI Designer',
                'Product Designer',
                'Digital Marketing Manager',
                'Content Strategist',
                'Sales Representative',
                'Account Executive',
                'Customer Support Specialist',
                'Technical Support Engineer',
                'DevOps Engineer',
                'Cloud Architect',
                'Product Manager',
                'Project Manager',
                'Business Analyst',
                'Quality Assurance Engineer',
            ]

            job_types = ['full_time', 'part_time', 'contract', 'internship', 'remote']
            experience_levels = ['entry', 'mid', 'senior', 'lead']

            for i in range(15):  # Create 15 sample jobs
                employer = random.choice(employers)
                company = random.choice(companies)
                category = random.choice(categories)

                job, created = Job.objects.get_or_create(
                    title=random.choice(job_titles),
                    employer=employer_user.employer_profile,
                    defaults={
                        'description': f"We are looking for a talented {random.choice(job_titles).lower()} to join our team. This is an exciting opportunity to work on challenging projects with a great team.",
                        'location': random.choice(['New York, NY', 'San Francisco, CA', 'Seattle, WA', 'Austin, TX', 'Boston, MA', 'Remote']),
                        'employment_type': random.choice(job_types),
                        'experience_level': random.choice(experience_levels),
                        'salary_min': random.randint(50000, 150000),
                        'salary_max': random.randint(150000, 250000),
                        'salary_currency': 'USD',
                        'category': category,
                        'status': 'published',
                        'application_deadline': timezone.now() + timezone.timedelta(days=30),
                    }
                )
                if created:
                    # Add some random skills to the job
                    skills = list(Skill.objects.all())
                    selected_skills = random.sample(skills, min(5, len(skills)))
                    job.skills.set(selected_skills)
                    self.stdout.write(f'Created job: {job.title} at {job.employer.user.username}\'s company')

        # Create some applications
        if job_seekers and Job.objects.exists():
            jobs = list(Job.objects.filter(status='published'))
            for job_seeker in job_seekers[:2]:  # First 2 job seekers apply to some jobs
                for job in random.sample(jobs, min(3, len(jobs))):  # Apply to 3 random jobs
                    application, created = Application.objects.get_or_create(
                        applicant=job_seeker,
                        job=job,
                        defaults={
                            'cover_letter': f"I am excited to apply for the {job.title} position at {job.employer.user.username}'s company. With my experience in {', '.join([s.name for s in job.skills.all()[:3]])}, I believe I would be a great fit for this role.",
                            'status': random.choice(['applied', 'reviewing', 'interview', 'offer', 'rejected', 'hired']),
                        }
                    )
                    if created:
                        self.stdout.write(f'Created application: {job_seeker.username} -> {job.title}')

        # Create some saved jobs
        if job_seekers and Job.objects.exists():
            jobs = list(Job.objects.filter(status='published'))
            for job_seeker in job_seekers:
                for job in random.sample(jobs, min(2, len(jobs))):  # Save 2 random jobs
                    saved_job, created = SavedJob.objects.get_or_create(
                        user=job_seeker,
                        job=job
                    )
                    if created:
                        self.stdout.write(f'Created saved job: {job_seeker.username} saved {job.title}')

        self.stdout.write(
            self.style.SUCCESS('Successfully created seed data!')
        )