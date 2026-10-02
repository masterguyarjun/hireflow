from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from .forms import CustomUserCreationForm, UserProfileForm, JobSeekerProfileForm, EmployerProfileForm
from .models import User, JobSeekerProfile, EmployerProfile


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"Welcome back, {user.username}!")
                return redirect('user_dashboard:home')
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'login_form': form})


def logout_view(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect('user_dashboard:home')


def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            account_type = form.cleaned_data.get('account_type')
            messages.success(request, f"Account created successfully for {user.username}!")

            # Create appropriate profile based on account type
            if account_type == 'job_seeker':
                JobSeekerProfile.objects.create(user=user)
            elif account_type == 'employer':
                EmployerProfile.objects.create(user=user)

            login(request, user)
            return redirect('user_dashboard:dashboard')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = CustomUserCreationForm()
    return render(request, 'accounts/register.html', {'register_form': form})


@login_required
def profile_view(request):
    if request.user.is_job_seeker:
        try:
            profile = request.user.job_seeker_profile
        except JobSeekerProfile.DoesNotExist:
            profile = JobSeekerProfile.objects.create(user=request.user)
        return render(request, 'accounts/profile.html', {'profile': profile, 'user_type': 'job_seeker'})
    elif request.user.is_employer:
        try:
            profile = request.user.employer_profile
        except EmployerProfile.DoesNotExist:
            profile = EmployerProfile.objects.create(user=request.user)
        return render(request, 'accounts/profile.html', {'profile': profile, 'user_type': 'employer'})
    else:
        return redirect('user_dashboard:home')


@login_required
def edit_profile_view(request):
    if request.user.is_job_seeker:
        try:
            profile = request.user.job_seeker_profile
        except JobSeekerProfile.DoesNotExist:
            profile = JobSeekerProfile.objects.create(user=request.user)

        if request.method == 'POST':
            user_form = UserProfileForm(request.POST, instance=request.user)
            profile_form = JobSeekerProfileForm(request.POST, request.FILES, instance=profile)
            if user_form.is_valid() and profile_form.is_valid():
                user_form.save()
                profile_form.save()
                messages.success(request, "Profile updated successfully!")
                return redirect('user_accounts:profile')
        else:
            user_form = UserProfileForm(instance=request.user)
            profile_form = JobSeekerProfileForm(instance=profile)
    elif request.user.is_employer:
        try:
            profile = request.user.employer_profile
        except EmployerProfile.DoesNotExist:
            profile = EmployerProfile.objects.create(user=request.user)

        if request.method == 'POST':
            user_form = UserProfileForm(request.POST, instance=request.user)
            profile_form = EmployerProfileForm(request.POST, request.FILES, instance=profile)
            if user_form.is_valid() and profile_form.is_valid():
                user_form.save()
                profile_form.save()
                messages.success(request, "Profile updated successfully!")
                return redirect('user_accounts:profile')
        else:
            user_form = UserProfileForm(instance=request.user)
            profile_form = EmployerProfileForm(instance=profile)
    else:
        return redirect('user_dashboard:home')

    return render(request, 'accounts/edit_profile.html', {
        'user_form': user_form,
        'profile_form': profile_form,
        'user_type': request.user.account_type
    })


@login_required
def change_password_view(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, "Your password was successfully updated!")
            return redirect('user_accounts:profile')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'accounts/change_password.html', {'form': form})