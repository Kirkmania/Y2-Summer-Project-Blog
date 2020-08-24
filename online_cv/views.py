from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from .forms import *
from blog.models import Post
from .models import *

# Create your views here.
@login_required
def cv_builder(request):
    form = CVForm()
    return render(request, 'online_cv/cv_builder.html', {'form': form})

def personal_details(request):
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
    if request.method == "POST":
        form = cvEducationForm(request.POST)
        if form.is_valid():
            cv_education = form.save(commit=False)
            cv_education.user = request.user
            cv_education.save()
            if 'education_save_and_add' in request.POST:
                return redirect('cv_education')
            return redirect('cv_work_history')
    else:
        form = cvEducationForm()
    return render(request, 'online_cv/education.html', {'form': form})

def work_history(request):
    if request.method == "POST":
        form = cvWorkHistoryForm(request.POST)
        if form.is_valid():
            cv_work_history = form.save(commit=False)
            cv_work_history.user = request.user
            cv_work_history.save()
            if 'work_history_save_and_add' in request.POST:
                return redirect('cv_work_history')
            return redirect('cv_extras')
    else:
        form = cvWorkHistoryForm()
    return render(request, 'online_cv/work_history.html', {'form': form})

def extras(request):
    if request.method == "POST":
        form = cvExtrasForm(request.POST)
        if form.is_valid():
            cv_extras = form.save(commit=False)
            cv_extras.user = request.user
            cv_extras.save()
            return redirect('cv_extras')
    else:
        try:
            extras = cvExtras.objects.get(user=request.user)
            if extras.skills == True:
                return redirect('cv_skills')
            elif extras.interests == True:
                return redirect('cv_interests')               
            elif extras.languages == True:
                return redirect('cv_languages')
            elif extras.certifications == True:
                return redirect('cv_certifications')     
        except ObjectDoesNotExist:
            form = cvExtrasForm()
        # except MultipleObjectsReturned:
    return render(request, 'online_cv/extras.html', {'form': form,})

def skills(request):
    if request.method == "POST":
        form = cvSkillForm(request.POST)
        if form.is_valid():
            cv_skill = form.save(commit=False)
            cv_skill.user = request.user
            cv_skill.save()
            extras = cvExtras.objects.get(user=request.user)
            if 'skill_add_another' in request.POST:
                return redirect('cv_skills')
            elif extras.interests == True:
                return redirect('cv_interests')               
            elif extras.languages == True:
                return redirect('cv_languages')
            elif extras.certifications == True:
                return redirect('cv_certifications')
    else:
        form = cvSkillForm()
    return render(request, 'online_cv/skills.html', {'form': form,})

def interests(request):
    if request.method == "POST":
        form = cvInterestForm(request.POST)
        if form.is_valid():
            cv_interest = form.save(commit=False)
            cv_interest.user = request.user
            cv_interest.save()
            extras = cvExtras.objects.get(user=request.user)
            if 'interest_add_another' in request.POST:
                return redirect('cv_interests')            
            elif extras.languages == True:
                return redirect('cv_languages')
            elif extras.certifications == True:
                return redirect('cv_certifications')
    else:
        form = cvInterestForm()
    return render(request, 'online_cv/interests.html', {'form': form,})

def languages(request):
    if request.method == "POST":
        form = cvLanguageForm(request.POST)
        if form.is_valid():
            cv_language = form.save(commit=False)
            cv_language.user = request.user
            cv_language.save()
            extras = cvExtras.objects.get(user=request.user)
            if 'language_add_another' in request.POST:
                return redirect('cv_languages')            
            elif extras.certifications == True:
                return redirect('cv_certifications')
    else:
        form = cvLanguageForm()
    return render(request, 'online_cv/languages.html', {'form': form,})

def certifications(request):
    if request.method == "POST":
        form = cvCertificationForm(request.POST)
        if form.is_valid():
            cv_certification = form.save(commit=False)
            cv_certification.user = request.user
            cv_certification.save()
            if 'certification_add_another' in request.POST:
                return redirect('cv_certifications')
            else:
                return redirect('cv_preview')
    else:
        form = cvCertificationForm()
    return render(request, 'online_cv/certifications.html', {'form': form,})

def preview(request):
    personal_details = cvPersonalDetails.objects.get(user=request.user)
    profile = cvProfile.objects.get(user=request.user)
    educations = cvEducation.objects.filter(user=request.user).order_by('-start_date')
    jobs = cvWorkHistory.objects.filter(user=request.user).order_by('-start_date')
    extras = cvExtras.objects.get(user=request.user)
    skills = cvSkill.objects.filter(user=request.user)
    interests = cvInterest.objects.filter(user=request.user)
    certifications = cvCertification.objects.filter(user=request.user).order_by('-date')
    languages = cvLanguage.objects.filter(user=request.user)

    return render(request, 'online_cv/preview.html', {
        'personal_details': personal_details,
        'profile': profile,
        'educations': educations,
        'jobs': jobs,
        'extras': extras,
        'skills': skills,
        'interests': interests,
        'certifications': certifications,
        'languages': languages,
    })