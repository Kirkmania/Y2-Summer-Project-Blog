from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.views.generic import TemplateView
from django.http import JsonResponse
from django.template.loader import render_to_string
from easy_pdf.rendering import render_to_pdf_response
from django_weasyprint import WeasyTemplateView
from .forms import *
from blog.models import Post
from .models import *

# Create your views here.
@login_required
def cv_builder(request):
    return render(request, 'online_cv/cv_builder.html')

@login_required
def start_new(request):
    educations = cvEducation.objects.filter(user=request.user).order_by('-start_date')
    jobs = cvWorkHistory.objects.filter(user=request.user).order_by('-start_date')
    skills = cvSkill.objects.filter(user=request.user)
    interests = cvInterest.objects.filter(user=request.user)
    certifications = cvCertification.objects.filter(user=request.user).order_by('-date')
    languages = cvLanguage.objects.filter(user=request.user)

    try:
        personal_details = cvPersonalDetails.objects.get(user=request.user)
    except ObjectDoesNotExist:
        personal_details = False
    try:
        profile = cvProfile.objects.get(user=request.user)
    except ObjectDoesNotExist:
        profile = False
    try:
        extras = cvExtras.objects.get(user=request.user)
    except ObjectDoesNotExist:
        extras = False

    if educations:
        for education in educations:
            education.delete()
    if jobs:
        for job in jobs:
            job.delete()
    if skills:
        for skill in skills:
            skill.delete()
    if interests:
        for interest in interests:
            interest.delete()
    if certifications:
        for certification in certifications:
            certification.delete()
    if languages:
        for language in languages:
            language.delete()
    if personal_details:
        personal_details.delete()
    if profile:
        profile.delete()
    if extras:
        extras.delete()

    return redirect('cv_personal_details')


@login_required
def personal_details(request):
    try: 
        personal_details = cvPersonalDetails.objects.get(user=request.user)
        if request.method == "POST":
            form = cvPersonalDetailsForm(request.POST, instance=personal_details)
            if form.is_valid():
                form.save()
                return redirect('cv_profile')
        else:
            form = cvPersonalDetailsForm(instance=personal_details)
        return render(request, 'online_cv/personal_details.html', {'form': form})
    except ObjectDoesNotExist:
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

@login_required
def profile(request):
    try: 
        profile = cvProfile.objects.get(user=request.user)
        if request.method == "POST":
            form = cvProfileForm(request.POST, instance=profile)
            if form.is_valid():
                form.save()
                return redirect('cv_education')
        else:
            form = cvProfileForm(instance=profile)
        return render(request, 'online_cv/profile.html', {'form': form})
    except ObjectDoesNotExist:
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

@login_required
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
            else:
                return redirect('cv_preview')
        except ObjectDoesNotExist:
            form = cvExtrasForm()
        # except MultipleObjectsReturned:
    return render(request, 'online_cv/extras.html', {'form': form,})

@login_required
def extras_edit(request):
    try:
        extras = cvExtras.objects.get(user=request.user)
    except:
        return redirect('cv_extras')
    if request.method == "POST":
        form = cvExtrasForm(request.POST, instance=extras)
        if form.is_valid():
            cv_extras = form.save(commit=False)
            cv_extras.user = request.user
            cv_extras.save()
            return redirect('cv_extras')
    else:
        form = cvExtrasForm(instance=extras)
        # except MultipleObjectsReturned:
    return render(request, 'online_cv/extras.html', {'form': form,})

################ Interests views ####################
@login_required
def interests(request):
    interests = cvInterest.objects.filter(user=request.user)
    return render(request, 'online_cv/interests.html', {'interests': interests})

@login_required
def save_interest_form(request, form, template_name):
    data = dict()

    if request.method == 'POST':
        if form.is_valid():
            cv_interest = form.save(commit=False)
            cv_interest.user = request.user
            cv_interest.save()
            data['form_is_valid'] = True
            interests = cvInterest.objects.filter(user=request.user)
            data['html_interest_list'] = render_to_string('online_cv/includes/interests/partial_interests_list.html', {
                'interests': interests
            })
        else:
            data['form_is_valid'] = False

    context = {'form': form}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)

@login_required
def interest_create(request):
    if request.method == 'POST':
        form = cvInterestForm(request.POST)
    else:
        form = cvInterestForm()
    return save_interest_form(request, form, 'online_cv/includes/interests/partial_interest_create.html')

@login_required
def interest_edit(request, pk):
    interest = get_object_or_404(cvInterest, pk=pk)
    if request.method == 'POST':
        form = cvInterestForm(request.POST, instance=interest)
    else:
        form = cvInterestForm(instance=interest)
    return save_interest_form(request, form, 'online_cv/includes/interests/partial_interest_edit.html')

@login_required
def interest_delete(request, pk):
    interest = get_object_or_404(cvInterest, pk=pk)
    data = dict()
    if request.method == 'POST':
        interest.delete()
        data['form_is_valid'] = True # Just to "play along" with the existing code
        interests = cvInterest.objects.filter(user=request.user)
        data['html_interest_list'] = render_to_string('online_cv/includes/interests/partial_interests_list.html', {
            'interests': interests
        })
    else:
        context = {'interest': interest}
        data['html_form'] = render_to_string('online_cv/includes/interests/partial_interest_delete.html',
            context,
            request=request,
        )
    return JsonResponse(data)

@login_required
def interest_next(request):
    try:
        extras = cvExtras.objects.get(user=request.user)             
        if extras.languages == True:
            return redirect('cv_languages')
        elif extras.certifications == True:
            return redirect('cv_certifications')
        else:
            return redirect('cv_preview')
    except ObjectDoesNotExist:
        return render(request, 'online_cv/extras_404.html')

################ Skills views ####################
@login_required
def skills(request):
    skills = cvSkill.objects.filter(user=request.user)
    return render(request, 'online_cv/skills.html', {'skills': skills})

@login_required
def save_skill_form(request, form, template_name):
    data = dict()

    if request.method == 'POST':
        if form.is_valid():
            cv_skill = form.save(commit=False)
            cv_skill.user = request.user
            cv_skill.save()
            data['form_is_valid'] = True
            skills = cvSkill.objects.filter(user=request.user)
            data['html_skill_list'] = render_to_string('online_cv/includes/skills/partial_skills_list.html', {
                'skills': skills
            })
        else:
            data['form_is_valid'] = False

    context = {'form': form}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)

@login_required
def skill_create(request):
    if request.method == 'POST':
        form = cvSkillForm(request.POST)
    else:
        form = cvSkillForm()
    return save_skill_form(request, form, 'online_cv/includes/skills/partial_skill_create.html')

@login_required
def skill_edit(request, pk):
    skill = get_object_or_404(cvSkill, pk=pk)
    if request.method == 'POST':
        form = cvSkillForm(request.POST, instance=skill)
    else:
        form = cvSkillForm(instance=skill)
    return save_skill_form(request, form, 'online_cv/includes/skills/partial_skill_edit.html')

@login_required
def skill_delete(request, pk):
    skill = get_object_or_404(cvSkill, pk=pk)
    data = dict()
    if request.method == 'POST':
        skill.delete()
        data['form_is_valid'] = True # Just to "play along" with the existing code
        skills = cvSkill.objects.filter(user=request.user)
        data['html_skill_list'] = render_to_string('online_cv/includes/skills/partial_skills_list.html', {
            'skills': skills
        })
    else:
        context = {'skill': skill}
        data['html_form'] = render_to_string('online_cv/includes/skills/partial_skill_delete.html',
            context,
            request=request,
        )
    return JsonResponse(data)

@login_required
def skill_next(request):
    try:
        extras = cvExtras.objects.get(user=request.user)   
        if extras.interests == True:
            return redirect('cv_interests')          
        elif extras.languages == True:
            return redirect('cv_languages')
        elif extras.certifications == True:
            return redirect('cv_certifications')
        else:
            return redirect('cv_preview')
    except ObjectDoesNotExist:
        return render(request, 'online_cv/extras_404.html')

################ Languages views ####################
@login_required
def languages(request):
    languages = cvLanguage.objects.filter(user=request.user)
    return render(request, 'online_cv/languages.html', {'languages': languages})

@login_required
def save_language_form(request, form, template_name):
    data = dict()

    if request.method == 'POST':
        if form.is_valid():
            cv_language = form.save(commit=False)
            cv_language.user = request.user
            cv_language.save()
            data['form_is_valid'] = True
            languages = cvLanguage.objects.filter(user=request.user)
            data['html_language_list'] = render_to_string('online_cv/includes/languages/partial_languages_list.html', {
                'languages': languages
            })
        else:
            data['form_is_valid'] = False

    context = {'form': form}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)

@login_required
def language_create(request):
    if request.method == 'POST':
        form = cvLanguageForm(request.POST)
    else:
        form = cvLanguageForm()
    return save_language_form(request, form, 'online_cv/includes/languages/partial_language_create.html')

@login_required
def language_edit(request, pk):
    language = get_object_or_404(cvLanguage, pk=pk)
    if request.method == 'POST':
        form = cvLanguageForm(request.POST, instance=language)
    else:
        form = cvLanguageForm(instance=language)
    return save_language_form(request, form, 'online_cv/includes/languages/partial_language_edit.html')

@login_required
def language_delete(request, pk):
    language = get_object_or_404(cvLanguage, pk=pk)
    data = dict()
    if request.method == 'POST':
        language.delete()
        data['form_is_valid'] = True # Just to "play along" with the existing code
        languages = cvLanguage.objects.filter(user=request.user)
        data['html_language_list'] = render_to_string('online_cv/includes/languages/partial_languages_list.html', {
            'languages': languages
        })
    else:
        context = {'language': language}
        data['html_form'] = render_to_string('online_cv/includes/languages/partial_language_delete.html',
            context,
            request=request,
        )
    return JsonResponse(data)

@login_required
def language_next(request):
    try:
        extras = cvExtras.objects.get(user=request.user)   
        if extras.certifications == True:
            return redirect('cv_certifications')
        else:
            return redirect('cv_preview')
    except ObjectDoesNotExist:
        return render(request, 'online_cv/extras_404.html')

################ Certifications views ####################
@login_required
def certifications(request):
    certifications = cvCertification.objects.filter(user=request.user)
    return render(request, 'online_cv/certifications.html', {'certifications': certifications})

@login_required
def save_certification_form(request, form, template_name):
    data = dict()

    if request.method == 'POST':
        if form.is_valid():
            cv_certification = form.save(commit=False)
            cv_certification.user = request.user
            cv_certification.save()
            data['form_is_valid'] = True
            certifications = cvCertification.objects.filter(user=request.user)
            data['html_certification_list'] = render_to_string('online_cv/includes/certifications/partial_certifications_list.html', {
                'certifications': certifications
            })
        else:
            data['form_is_valid'] = False

    context = {'form': form}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)

@login_required
def certification_create(request):
    if request.method == 'POST':
        form = cvCertificationForm(request.POST)
    else:
        form = cvCertificationForm()
    return save_certification_form(request, form, 'online_cv/includes/certifications/partial_certification_create.html')

@login_required
def certification_edit(request, pk):
    certification = get_object_or_404(cvCertification, pk=pk)
    if request.method == 'POST':
        form = cvCertificationForm(request.POST, instance=certification)
    else:
        form = cvCertificationForm(instance=certification)
    return save_certification_form(request, form, 'online_cv/includes/certifications/partial_certification_edit.html')

@login_required
def certification_delete(request, pk):
    certification = get_object_or_404(cvCertification, pk=pk)
    data = dict()
    if request.method == 'POST':
        certification.delete()
        data['form_is_valid'] = True # Just to "play along" with the existing code
        certifications = cvCertification.objects.filter(user=request.user)
        data['html_certification_list'] = render_to_string('online_cv/includes/certifications/partial_certifications_list.html', {
            'certifications': certifications
        })
    else:
        context = {'certification': certification}
        data['html_form'] = render_to_string('online_cv/includes/certifications/partial_certification_delete.html',
            context,
            request=request,
        )
    return JsonResponse(data)

################ Educations views ####################
@login_required
def educations(request):
    educations = cvEducation.objects.filter(user=request.user)
    return render(request, 'online_cv/education.html', {'educations': educations})

@login_required
def save_education_form(request, form, template_name):
    data = dict()

    if request.method == 'POST':
        if form.is_valid():
            cv_education = form.save(commit=False)
            cv_education.user = request.user
            cv_education.save()
            data['form_is_valid'] = True
            educations = cvEducation.objects.filter(user=request.user)
            data['html_education_list'] = render_to_string('online_cv/includes/educations/partial_educations_list.html', {
                'educations': educations
            })
        else:
            data['form_is_valid'] = False

    context = {'form': form}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)

@login_required
def education_create(request):
    if request.method == 'POST':
        form = cvEducationForm(request.POST)
    else:
        form = cvEducationForm()
    return save_education_form(request, form, 'online_cv/includes/educations/partial_education_create.html')

@login_required
def education_edit(request, pk):
    education = get_object_or_404(cvEducation, pk=pk)
    if request.method == 'POST':
        form = cvEducationForm(request.POST, instance=education)
    else:
        form = cvEducationForm(instance=education)
    return save_education_form(request, form, 'online_cv/includes/educations/partial_education_edit.html')

@login_required
def education_delete(request, pk):
    education = get_object_or_404(cvEducation, pk=pk)
    data = dict()
    if request.method == 'POST':
        education.delete()
        data['form_is_valid'] = True # Just to "play along" with the existing code
        educations = cvEducation.objects.filter(user=request.user)
        data['html_education_list'] = render_to_string('online_cv/includes/educations/partial_educations_list.html', {
            'educations': educations
        })
    else:
        context = {'education': education}
        data['html_form'] = render_to_string('online_cv/includes/educations/partial_education_delete.html',
            context,
            request=request,
        )
    return JsonResponse(data)

################ Work History views ####################
@login_required
def jobs(request):
    jobs = cvWorkHistory.objects.filter(user=request.user)
    return render(request, 'online_cv/job.html', {'jobs': jobs})

@login_required
def save_job_form(request, form, template_name):
    data = dict()

    if request.method == 'POST':
        if form.is_valid():
            cv_job = form.save(commit=False)
            cv_job.user = request.user
            cv_job.save()
            data['form_is_valid'] = True
            jobs = cvWorkHistory.objects.filter(user=request.user)
            data['html_job_list'] = render_to_string('online_cv/includes/jobs/partial_jobs_list.html', {
                'jobs': jobs
            })
        else:
            data['form_is_valid'] = False

    context = {'form': form}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)

@login_required
def job_create(request):
    if request.method == 'POST':
        form = cvWorkHistoryForm(request.POST)
    else:
        form = cvWorkHistoryForm()
    return save_job_form(request, form, 'online_cv/includes/jobs/partial_job_create.html')

@login_required
def job_edit(request, pk):
    job = get_object_or_404(cvWorkHistory, pk=pk)
    if request.method == 'POST':
        form = cvWorkHistoryForm(request.POST, instance=job)
    else:
        form = cvWorkHistoryForm(instance=job)
    return save_job_form(request, form, 'online_cv/includes/jobs/partial_job_edit.html')

@login_required
def job_delete(request, pk):
    job = get_object_or_404(cvWorkHistory, pk=pk)
    data = dict()
    if request.method == 'POST':
        job.delete()
        data['form_is_valid'] = True # Just to "play along" with the existing code
        jobs = cvWorkHistory.objects.filter(user=request.user)
        data['html_job_list'] = render_to_string('online_cv/includes/jobs/partial_jobs_list.html', {
            'jobs': jobs
        })
    else:
        context = {'job': job}
        data['html_form'] = render_to_string('online_cv/includes/jobs/partial_job_delete.html',
            context,
            request=request,
        )
    return JsonResponse(data)

####################### PREVIEW AND PDFVIEW AT LAST ############################
@login_required
def preview(request):
    educations = cvEducation.objects.filter(user=request.user).order_by('-start_date')
    jobs = cvWorkHistory.objects.filter(user=request.user).order_by('-start_date')
    skills = cvSkill.objects.filter(user=request.user)
    interests = cvInterest.objects.filter(user=request.user)
    certifications = cvCertification.objects.filter(user=request.user).order_by('-date')
    languages = cvLanguage.objects.filter(user=request.user)

    try:
        personal_details = cvPersonalDetails.objects.get(user=request.user)
    except ObjectDoesNotExist:
        personal_details = False
    try:
        profile = cvProfile.objects.get(user=request.user)
    except ObjectDoesNotExist:
        profile = False

    try:
        extras = cvExtras.objects.get(user=request.user)
    except ObjectDoesNotExist:
        extras = False

    context = {
        'personal_details': personal_details,
        'profile': profile,
        'educations': educations,
        'jobs': jobs,
        'extras': extras,
        'skills': skills,
        'interests': interests,
        'certifications': certifications,
        'languages': languages,
    }

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

class ExportPDF(WeasyTemplateView):
    
    template_name='online_cv/export.html'

    def get_context_data(self, **kwargs):
        context = super(ExportPDF, self).get_context_data(**kwargs)

        self.educations = cvEducation.objects.filter(user=self.request.user).order_by('-start_date')
        self.jobs = cvWorkHistory.objects.filter(user=self.request.user).order_by('-start_date')
        self.skills = cvSkill.objects.filter(user=self.request.user)
        self.interests = cvInterest.objects.filter(user=self.request.user)
        self.certifications = cvCertification.objects.filter(user=self.request.user).order_by('-date')
        self.languages = cvLanguage.objects.filter(user=self.request.user)

        try:
            self.personal_details = cvPersonalDetails.objects.get(user=self.request.user)
        except ObjectDoesNotExist:
            self.personal_details = False
        try:
            self.profile = cvProfile.objects.get(user=self.request.user)
        except ObjectDoesNotExist:
            self.profile = False

        try:
            self.extras = cvExtras.objects.get(user=self.request.user)
        except ObjectDoesNotExist:
            self.extras = False

        context['educations'] = self.educations
        context['jobs'] = self.jobs
        context['skills'] = self.skills
        context['interests'] = self.interests
        context['certifications'] = self.certifications
        context['languages'] = self.languages
        context['personal_details'] = self.personal_details
        context['profile'] = self.profile
        context['extras'] = self.extras

        return context