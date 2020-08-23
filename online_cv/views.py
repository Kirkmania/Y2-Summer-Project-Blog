from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from .forms import *
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
            # elif extras.interests == True:
            #     return redirect('cv_interests')
            # elif extras.languages == True:
            #     return redirect('cv_languages')
            # elif extras.certifications == True:
            #     return redirect('cv_certifications')
        except ObjectDoesNotExist:
            form = cvExtrasForm()
        # except MultipleObjectsReturned:
    return render(request, 'online_cv/extras.html', {'form': form,})

def skills(request):
    if request.method == "POST":
        form = cvSkillsForm(request.POST)
        if form.is_valid():
            cv_skills = form.save(commit=False)
            cv_skills.user = request.user
            cv_skills.save()
            extras = cvExtras.objects.get(user=request.user)
            if extras.interests == True:
                return redirect('cv_builder')               
            # elif extras.languages == True:
            #     return redirect('cv_languages')
            # elif extras.certifications == True:
            #     return redirect('cv_certifications')
    else:
        form = cvSkillsForm()
    return render(request, 'online_cv/skills.html', {'form': form,})