from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import CVForm, cvPersonalDetailsForm, cvProfileForm, cvEducationForm
from .models import CV, cvPersonalDetails, cvProfile, cvEducation

# Create your views here.
@login_required
def cv_builder(request):
    form = CVForm()
    return render(request, 'online_cv/cv_builder.html', {'form': form})

def personal_details(request):
    form = cvPersonalDetailsForm()
    if request.method == "POST":
        form = cvPersonalDetailsForm(request.POST)
        if form.is_valid():
            cv_personal_details = form.save(commit=False)
            cv_personal_details.user = request.user
            cv_personal_details.save()
            return redirect('cv_profile')
    else:
        form = cvPersonalDetailsForm()
    return render(request, 'online_cv/personal_details.html', {'form': form})

def profile(request):
    form = cvProfileForm()
    if request.method == "POST":
        form = cvProfileForm(request.POST)
        if form.is_valid():
            cv_profile = form.save(commit=False)
            cv_profile.user = request.user
            cv_profile.save()
            return redirect('cv_education')
    else:
        form = cvProfileForm()
    return render(request, 'online_cv/profile.html', {'form': form})

def education(request):
    form = cvEducationForm()
    if request.method == "POST":
        form = cvEducationForm(request.POST)
        if form.is_valid():
            cv_education = form.save(commit=False)
            cv_education.user = request.user
            cv_education.save()
            if 'add_another' in request.POST:
                return redirect('cv_education')
            return redirect('cv_builder')
    else:
        form = cvEducationForm()
    return render(request, 'online_cv/education.html', {'form': form})