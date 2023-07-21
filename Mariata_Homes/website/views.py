from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.conf import settings
from django.core.mail import send_mail
from django.contrib import messages

from .models import Admin, Applicant, Source, Notification

from .dataforms import ApplicantSignUpForm, LoginForm, ApplicantStatusForm, ApplicantUpdateForm, ApplicantDeleteForm, EmailForm

def signup(request):
    if(Admin.objects.count() == 0):
        Admin.objects.create(username='admin', password='admin')
    if request.method == 'POST':
        form = ApplicantSignUpForm(request.POST, request.FILES)
        if form.is_valid():
            applicant = form.save(commit=False)
            applicant.status = 'pending'
            applicant.save()
            print(applicant)
            render(request, 'signup.html', {'form': form})
    form = ApplicantSignUpForm()
    return render(request, 'signup.html', {'form': form})

def login(request):
    if request.method == 'POST':
        message = None
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            p = None
            try:
                p = Admin.objects.get(username=username)
                if p.password==password:
                    request.session['user_id'] = p.username
                    return HttpResponseRedirect('admin.html')
                else:
                    message = "Invalid username or password"
            except (Admin.DoesNotExist):
                message = "Invalid username"
            
            return render(request, 'login.html', {'form': form,'message':message})
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

def logout(request):
    form = LoginForm()
    request.session['user_id'] = None
    return render(request, 'login.html', {'form': form})

def admin(request):
    out = Applicant.objects.all()
    return render(request, 'admin.html', {'out': out})

def approve(request):
    form = ApplicantStatusForm(request.POST or None)
    if form.is_valid():
        email = form.cleaned_data['email']
        status = form.cleaned_data['status']
        try:
            applicant = Applicant.objects.get(email=email)
            applicant.status = status
            applicant.save()
            print(applicant.email)
            print(applicant.status)
            out = Applicant.objects.all()
            return render(request, 'admin.html', {'out': out})
        except Applicant.DoesNotExist:
            message = "No applicant found with that email."
            return render(request, 'approve.html', {'form':form,'message': message})
    context = {
        'form': form,
    }
    return render(request, 'approve.html', context)

def update(request):
    if request.method == 'POST':
        form = ApplicantUpdateForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            applicant = Applicant.objects.get(email=email)

            # Update fields based on the form data
            if form.cleaned_data.get('name'):
                applicant.name = form.cleaned_data.get('name')
            if form.cleaned_data.get('dob'):
                applicant.dob = form.cleaned_data.get('dob')
            if form.cleaned_data.get('phone'):
                applicant.phone = form.cleaned_data.get('phone')
            if form.cleaned_data.get('illnesses'):
                applicant.illnesses = form.cleaned_data.get('illnesses')
            if form.cleaned_data.get('disabilities'):
                applicant.disabilities = form.cleaned_data.get('disabilities')
            if form.cleaned_data.get('last_residence'):
                applicant.last_residence = form.cleaned_data.get('last_residence')
            if form.cleaned_data.get('next_of_kin'):
                applicant.next_of_kin = form.cleaned_data.get('next_of_kin')
            if form.cleaned_data.get('recommendation'):
                applicant.recommendation = form.cleaned_data.get('recommendation')
            if form.cleaned_data.get('status'):
                applicant.status = form.cleaned_data.get('status')

            applicant.save()
            out = Applicant.objects.all()
            return render(request, 'admin.html', {'out': out})
        
    form = ApplicantUpdateForm()
    return render(request, 'update.html', {'form': form})

def delete(request):
    if request.method == 'POST':
        form = ApplicantDeleteForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            if Applicant.objects.filter(email=email):
                Applicant.objects.filter(email=email).delete()
                out = Applicant.objects.all()
                return render(request, 'admin.html', {'out': out})
            else:
                message = 'No Such Applicant Exists.'
                return render(request,'delete.html',{'form':form,'message':message})
    form = ApplicantDeleteForm()
    return render(request, 'delete.html',{'form':form})


def send_email(request):
    if request.method == 'POST':
        form = EmailForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']
            subject = "Application Status: Mariata Homes"
            send_mail(subject, message, settings.EMAIL_HOST_USER, [email], fail_silently=False, auth_user=settings.EMAIL_HOST_USER, auth_password=settings.EMAIL_HOST_PASSWORD, connection=None, html_message=None)
            return HttpResponseRedirect('admin.html')
    else:
        form = EmailForm()
    return render(request, 'notification.html', {'form': form})