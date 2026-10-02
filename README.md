# HireFlow

Modern Job Portal built with Django and PostgreSQL.

HireFlow is a full-featured job portal platform that connects job seekers with employers. Built with Django, it provides a seamless experience for both parties - job seekers can search and apply for positions, while employers can post jobs, manage applications, and find qualified candidates.

---

## 🚀 Features

### Authentication & User Management
- User registration with account type selection (Job Seeker or Employer)
- Secure login/logout functionality
- Password change and reset capabilities
- Profile management for both job seekers and employers
- Custom user model with extended fields (phone number, date of birth, etc.)

### Job Seeker Features
- Job search with full-text search across title, description, company, location, and skills
- Advanced filtering by location, remote options, employment type, experience level, category, skills, and salary range
- Sorting options (newest, oldest, salary low to high, salary high to low)
- Job bookmarking/saving functionality
- Job application system with resume upload and cover letter
- Application tracking with status updates (Submitted, Under Review, Shortlisted, Interview, Rejected, Hired)
- Personal dashboard showing application statistics and recent activity
- Resume upload with file type validation (PDF, DOC, DOCX) and size limits (5MB)

### Employer Features
- Company profile management with logo, description, website, location, size, and industry
- Job creation and management (CRUD operations)
- Job publishing workflow (draft → published → closed)
- Application management for posted jobs
- Application status updates (Submitted, Under Review, Shortlisted, Interview, Rejected, Hired)
- Internal notes on applications
- Employer dashboard showing job statistics and recent applications
- Featured job highlighting capability

### Job Management
- Full CRUD operations for job postings
- Categorization system with Categories and Skills models
- Flexible employment types (Full Time, Part Time, Contract, Internship, Temporary)
- Remote work options (On-site, Hybrid, Remote)
- Experience level classifications (Entry Level, Mid Level, Senior Level, Lead, Executive)
- Salary range specification with currency selection
- Application deadline management
- Job status tracking (Draft, Published, Closed)
- Featured job flagging
- Responsibilities, requirements, and benefits fields

### Security
- Django's built-in authentication system with CSRF protection
- Role-based authorization (Job Seeker, Employer, Admin)
- Custom user model to prevent auth.User conflicts
- File upload validation (type and size limits)
- Environment-based configuration for secrets
- Production-ready security settings (HTTPS redirects, secure cookies, HSTS)
- SQL injection protection via Django ORM
- Input validation and sanitization through Django forms
- Permission checks on all sensitive operations

---

## 🛠️ Tech Stack

- **Backend**: Python, Django 4.2+
- **Database**: PostgreSQL (with SQLite fallback for development)
- **Frontend**: HTML5, CSS3, Bootstrap 5, JavaScript
- **Deployment**: Gunicorn, WhiteNoise
- **Development Tools**: Git/GitHub, Python virtual environment
- **File Handling**: Pillow (for image uploads)

---

## 📁 Project Structure

```
hireflow/
├── config/                    # Django project settings
│   ├── settings.py           # Project configuration
│   ├── urls.py               # URL routing
│   └── wsgi.py               # WSGI configuration
├── company_profiles/          # Company profile management
│   ├── models.py             # Company model
│   ├── views.py              # Company views
│   └── urls.py               # Company URLs
├── job_applications/          # Job application system
│   ├── models.py             # Application model
│   ├── forms.py              # Application forms
│   ├── views.py              # Application views
│   └── urls.py               # Application URLs
├── job_listings/             # Job listing and management
│   ├── models.py             # Job, Category, Skill models
│   ├── forms.py              # Job forms
│   ├── views.py              # Job views
│   └── urls.py               # Job URLs
├── user_accounts/            # User authentication and profiles
│   ├── models.py             # Custom User model, JobSeekerProfile, EmployerProfile
│   ├── forms.py              # Registration and profile forms
│   ├── views.py              # Authentication views
│   └── urls.py               # Account URLs
├── user_dashboard/           # Dashboard functionality
│   ├── models.py             # SavedJob model
│   ├── views.py              # Dashboard views (seeker, employer, admin)
│   └── urls.py               # Dashboard URLs
├── static/                   # Static assets (CSS, JS, Images)
├── templates/                # HTML templates
│   ├── accounts/             # Authentication templates
│   ├── applications/         # Application templates
│   ├── dashboard/            # Dashboard templates
│   └── jobs/                 # Job listing templates
├── manage.py                 # Django management script
├── requirements.txt          # Python dependencies
├── Procfile                  # Heroku/Render process declaration
├── runtime.txt               # Python version specification
├── .env.example              # Environment variables template
└── README.md                 # Project documentation
```

### Key Apps Description:
- **company_profiles**: Manages employer company profiles and verification
- **job_applications**: Handles job applications, resume uploads, and status tracking
- **job_listings**: Manages job postings, search, filtering, and categorization
- **user_accounts**: Custom user model with role-based profiles (job seeker/employer)
- **user_dashboard**: Homepage, dashboards for different user types, and saved jobs functionality

---

## 🗄️ Database / Data Model

### Core Entities:

**User** (Custom Model)
- Extends Django's AbstractUser
- Account type selection: job_seeker, employer, admin
- Additional fields: phone number, date of birth

**JobSeekerProfile**
- One-to-one with User (for job seekers)
- Professional headline, bio, skills (comma-separated)
- Years of experience, education, current job title
- Location, social media links (LinkedIn, GitHub, Portfolio)
- Resume file upload

**EmployerProfile**
- One-to-one with User (for employers)
- Company name, logo, description, website, location
- Industry, company size, contact email
- LinkedIn URL

**Company** (Additional employer info)
- One-to-one with EmployerProfile
- Founded year, headquarters, specialties, culture description
- Verification status

**Job**
- Foreign key to EmployerProfile
- Title, slug, detailed description
- Location, remote option (on-site/hybrid/remote)
- Employment type, experience level
- Salary range (min/max) with currency
- Foreign key to Category, Many-to-many to Skills
- Responsibilities, requirements, benefits
- Application deadline
- Status (draft/published/closed)
- Published timestamp, featured flag

**Category**
- Job classifications (e.g., Engineering, Design, Marketing)

**Skill**
- Technical skills that can be associated with jobs

**Application**
- Foreign key to Job and User (applicant)
- Resume upload (PDF/DOC/DOCX validated)
- Cover letter
- Status tracking (submitted/under_review/shortlisted/interview/rejected/hired)
- Application timestamp
- Employer notes field
- Unique constraint: one application per user per job

**SavedJob**
- Many-to-many between User and Job (with timestamp)
- Prevents duplicate saves

### Key Relationships:
- User → JobSeekerProfile/EmployerProfile (One-to-one)
- EmployerProfile → Company (One-to-one)
- EmployerProfile → Job (One-to-many)
- Job → Application (One-to-many)
- User → Application (One-to-many)
- Job → Category (Many-to-one)
- Job → Skill (Many-to-many)
- User → SavedJob (Many-to-many)
- Job → SavedJob (Many-to-many)

---

## 👥 User Roles

### Job Seeker
Can:
- Register and create job seeker profile
- Search and filter jobs using multiple criteria
- View detailed job listings
- Save/bookmark jobs for later reference
- Apply for jobs with resume and cover letter
- Track application status and history
- Update personal profile and resume
- Change password
- Access job seeker dashboard with application statistics

### Employer
Can:
- Register and create employer profile
- Manage company profile information
- Create, edit, and delete job postings
- Save jobs as drafts before publishing
- Publish and close job postings
- View all applications for their jobs
- Update application status with predefined options
- Add internal notes to applications
- Access employer dashboard with job and application statistics

### Administrator
Can:
- Access Django admin interface
- Manage all users (job seekers, employers, admins)
- View system-wide statistics
- Perform all actions available to job seekers and employers
- Access admin dashboard with platform analytics

---

## 🔎 Search & Filtering

### Search Fields
The job search functionality searches across:
- Job title (partial match)
- Job description (partial match)
- Company name (partial match)
- Job location (partial match)
- Skill names (partial match)
- Category names (partial match)

### Available Filters
- **Location**: Text-based filtering (icontains match)
- **Remote Option**: On-site, Hybrid, or Remote
- **Employment Type**: Full Time, Part Time, Contract, Internship, Temporary
- **Experience Level**: Entry Level, Mid Level, Senior Level, Lead, Executive
- **Category**: Dropdown selection from available categories
- **Skills**: Multiple skill selection (jobs must have ALL selected skills)
- **Salary Range**: Minimum and maximum salary filters
- **Date Posted**: Jobs posted within last X days (7, 14, 30, 60)

### Sorting Options
- Newest first (default)
- Oldest first
- Salary: Low to High
- Salary: High to Low

### Pagination
- 10 jobs per page in job listings
- Page numbers displayed at bottom of results

---

## 📋 Application Workflow

### Job Seeker Perspective:
1. **Registration**: Sign up selecting "Job Seeker" account type
2. **Profile Setup**: Complete job seeker profile with skills, experience, resume
3. **Job Discovery**: Search or browse jobs using filters and search
4. **Job Review**: Click on job to view full details
5. **Application**: Click "Apply Now" button, upload resume, write cover letter
6. **Confirmation**: Application submitted successfully
7. **Tracking**: View application status in "My Applications" section
8. **Updates**: Receive status changes as employer reviews application

### Employer Perspective:
1. **Registration**: Sign up selecting "Employer" account type
2. **Profile Setup**: Complete employer profile with company details
3. **Job Creation**: Create new job posting (starts as draft)
4. **Review/Publish**: Review job details and publish when ready
5. **Application Management**: View incoming applications in dashboard
6. **Review Applications**: Examine applicant resumes and cover letters
7. **Status Updates**: Update application status as hiring process progresses
8. **Communication**: Use employer notes for internal tracking
9. **Closing**: Close position when filled or no longer accepting applications

### Application Statuses:
- **Submitted**: Application received
- **Under Review**: Employer is reviewing applications
- **Shortlisted**: Candidate selected for next round
- **Interview**: Candidate scheduled for/completed interview
- **Rejected**: Application not successful
- **Hired**: Candidate selected for position

---

## 🔐 Security

HireFlow implements multiple security layers:

### Authentication & Authorization
- Django's secure authentication system with password hashing
- Role-based access control preventing unauthorized access
- Permission checks on all sensitive views (job creation, application updates, etc.)
- Custom user model to avoid conflicts with Django's auth.User

### Data Protection
- SQL injection prevention through Django ORM usage
- Cross-site request forgery (CSRF) protection on all forms
- Clickjacking protection via X-Frame-Options
- Content type nosniff protection
- XSS protection headers

### File Upload Security
- Resume upload limited to PDF, DOC, DOCX formats only
- File size restriction (5MB maximum)
- Server-side validation of file extensions and MIME types
- Safe file storage through Django's FileField

### Configuration Security
- Environment-based configuration for secrets (SECRET_KEY, database credentials)
- Debug mode disabled in production
- Secret key management through environment variables
- Allowed hosts configuration
- Secure cookie settings in production
- HTTP to HTTPS redirect in production
- HSTS (HTTP Strict Transport Security) enabled
- Referrer policy and other security headers

### Environment Variables Required:
- `SECRET_KEY`: Django secret key (keep secret!)
- `DEBUG`: Set to False in production
- `ALLOWED_HOSTS`: Comma-separated list of allowed domains
- `DATABASE_URL`: PostgreSQL connection string (overrides SQLite default)

### Important Security Notes:
- Never commit `.env` file containing real secrets to version control
- Always use environment variables for production secrets
- Keep SECRET_KEY confidential - it's used for cryptographic signing
- In production, ensure DEBUG=False to prevent information leakage
- Regularly update dependencies to patch known vulnerabilities

---

## ⚙️ Installation

Follow these steps to set up HireFlow locally:

### 1. Clone repository
```bash
git clone https://github.com/masterguyarjun/hireflow.git
cd hireflow
```

### 2. Create virtual environment
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure environment
```bash
cp .env.example .env
```
Edit `.env` file and add your actual values:
- `SECRET_KEY`: Generate a secure secret key
- `DEBUG`: Set to `True` for development, `False` for production
- `ALLOWED_HOSTS`: Add your domain(s) (e.g., `localhost,127.0.0.1,yourdomain.com`)
- For PostgreSQL: Set `DATABASE_URL` or use individual DB_* variables

### 5. Database Setup
HireFlow supports both SQLite (development) and PostgreSQL (production):

#### Option A: SQLite (Development - Default)
No additional setup needed - SQLite database will be created automatically.

#### Option B: PostgreSQL (Production/Development)
1. Install PostgreSQL if not already installed
2. Create a database: `createdb hireflow`
3. Create a user: `createuser -s postgres` (or use existing postgres user)
4. Set password for user: `ALTER USER postgres WITH PASSWORD 'your_password';`
5. Configure `.env` with PostgreSQL connection:
   ```
   DATABASE_URL=postgres://postgres:your_password@localhost:5432/hireflow
   ```
   OR set individual variables:
   ```
   DB_NAME=hireflow
   DB_USER=postgres
   DB_PASSWORD=your_password
   DB_HOST=localhost
   DB_PORT=5432
   ```

### 6. Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 7. Create admin superuser
```bash
python manage.py createsuperuser
```
Follow the prompts to create your administrator account.

### 8. Run development server
```bash
python manage.py runserver
```
Visit `http://127.0.0.1:8000/` in your browser to access the application.

---

## ▶️ Usage

### Job Seeker Workflow:
1. Visit homepage and click "Register"
2. Select "Job Seeker" as account type
3. Fill in registration form and submit
4. Complete your job seeker profile (skills, experience, resume upload)
5. Use search bar and filters to find relevant jobs
6. Click on job listings to view full details
7. Click "Apply Now" on jobs you're interested in
8. Upload your resume and write a cover letter
9. Track your applications in the "My Applications" section
10. Update your profile and resume as needed

### Employer Workflow:
1. Visit homepage and click "Register"
2. Select "Employer" as account type
3. Fill in registration form and submit
4. Complete your employer profile (company details, logo, etc.)
5. Click "Create Job" to post a new position
6. Fill in job details (title, description, requirements, etc.)
7. Set salary range, application deadline, and other job specifics
8. Save as draft or publish immediately
9. Manage incoming applications from your employer dashboard
10. Update application status as candidates progress through hiring process
11. Add internal notes to applications for team collaboration
12. Close positions when filled or no longer accepting applications

### Administrator Access:
1. Create superuser account using `createsuperuser` command
2. Login at `/admin/` with your superuser credentials
3. Manage users, jobs, applications, and system settings
4. View analytics and platform statistics in admin dashboard

---

## 🧪 Testing

The project currently includes Django test files in each app directory, but no automated tests have been implemented yet. The test files are placeholders ready for future test development.

To run tests when they are implemented:
```bash
python manage.py test
```

For now, manual testing is recommended to verify functionality.

---

## 🚀 Production Deployment

HireFlow is configured for deployment to platforms like Render, Heroku, or any Django-compatible hosting service.

### Render Deployment Instructions:
1. Create PostgreSQL database in Render dashboard
2. Connect your GitHub repository to Render
3. Configure build command: `pip install -r requirements.txt`
4. Configure start command: `gunicorn config.wsgi:application`
5. Set environment variables in Render dashboard:
   - `SECRET_KEY`: Your secure secret key
   - `DEBUG`: `False`
   - `ALLOWED_HOSTS`: Your Render domain (e.g., `your-app.onrender.com`)
   - `DATABASE_URL`: Render will provide this automatically when you add PostgreSQL
6. Enable "Auto Deploy" for automatic updates on git push
7. Trigger first deploy
8. After deployment, run migrations manually or add to deploy script:
   ```bash
   python manage.py migrate
   python manage.py createsuperuser  # Create admin account
   ```

### Generic Deployment Steps:
1. Provision PostgreSQL database
2. Set environment variables (SECRET_KEY, DEBUG=False, ALLOWED_HOSTS, DATABASE_URL)
3. Pull/push code to server
4. Install dependencies: `pip install -r requirements.txt`
5. Collect static files: `python manage.py collectstatic`
6. Run migrations: `python manage.py migrate`
7. Create superuser: `python manage.py createsuperuser`
8. Start application: `gunicorn config.wsgi:application`
9. Configure reverse proxy (Nginx/Apache) if needed
10. Set up process manager (systemd, PM2, etc.) for automatic restarts

---

## 🔑 Environment Variables

| Variable | Purpose | Required | Default/Example |
|----------|---------|----------|-----------------|
| SECRET_KEY | Django secret key for cryptographic signing | Yes | Generate with `django.core.management.utils.get_random_secret_key()` |
| DEBUG | Development/production mode toggle | Yes | `True` (dev), `False` (prod) |
| ALLOWED_HOSTS | Comma-separated list of allowed domains | Yes | `localhost,127.0.0.1` (dev) |
| DATABASE_URL | PostgreSQL connection string (overrides SQLite) | No (SQLite default) | `postgres://user:pass@host:5432/dbname` |
| DB_NAME | Database name (if not using DATABASE_URL) | No* | `hireflow` |
| DB_USER | Database username (if not using DATABASE_URL) | No* | `postgres` |
| DB_PASSWORD | Database password (if not using DATABASE_URL) | No* | `postgres` |
| DB_HOST | Database host (if not using DATABASE_URL) | No* | `localhost` |
| DB_PORT | Database port (if not using DATABASE_URL) | No* | `5432` |

\* Individual DB_* variables are only required if DATABASE_URL is not set.

---

## 📸 Screenshots

Add screenshots here showing:
- Homepage with featured jobs
- Job listing/search page with filters
- Individual job detail page
- User registration and login pages
- Job seeker dashboard with application statistics
- Employer dashboard with job management
- Application submission form
- Employer application review interface

*(Screenshot placeholders - add actual images after deployment)*

---

## 🌐 Live Demo

Live Demo: Not deployed yet

GitHub:
https://github.com/masterguyarjun/hireflow

---

## 🧑‍💻 Project Information

**Project:** HireFlow  
**Type:** Full-Stack Job Portal  
**Backend:** Django 4.2+  
**Database:** PostgreSQL (SQLite for development)  
**Frontend:** HTML5, CSS3, Bootstrap 5, JavaScript  
**Repository:** https://github.com/masterguyarjun/hireflow  

---

## 📌 Future Improvements

These are planned enhancements for future development:

- **Email Notifications**: Automated emails for application status updates, new job alerts, etc.
- **Advanced Job Alerts**: Saved search notifications for job seekers
- **Resume Parsing**: Automatic extraction of skills/experience from uploaded resumes
- **REST API**: API for mobile apps or third-party integrations
- **OAuth Authentication**: Google/Facebook/LinkedIn login options
- **Interview Scheduling**: Built-in calendar and scheduling for interviews
- **Recommendation Engine**: AI-powered job recommendations based on profile/skills
- **Advanced Analytics**: Employer analytics on job performance and applicant demographics
- **Mobile Responsive Design**: Enhanced mobile experience
- **Application Tracking**: Timeline view of application progress
- **Skill Assessment**: Built-in skill testing for candidates
- **Video Interviewing**: Integrated video call functionality
- **Multi-language Support**: Internationalization for global users
- **Employer Branding**: Enhanced company pages with videos, culture info, etc.

---

## 📄 License

No license specified in the repository. Please check with the project owner for usage rights and distribution terms.