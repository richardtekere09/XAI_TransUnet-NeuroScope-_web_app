from .forms import MRIScanForm
from .models import MRI_Scan , Doctor
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from django.templatetags.static import static
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
import json
from .forms import UserUpdateForm, ProfileUpdateForm
from groq import Groq
import os

client = Groq(api_key=os.getenv('GROQ_API_KEY'))

# Create your views here.
#home view
def home(request):
    return render(request, 'home.html')

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

# Initialize the Groq client
client = Groq(api_key=os.getenv('GROQ_API_KEY'))


# Signup View
def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # Redirect to login page after successful signup
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})


def neurocheck_view(request):
    return render(request, 'neurocheck.html')

@csrf_exempt
def neurocheck_chat(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_message = data.get('message')

            if not user_message:
                return JsonResponse({'error': 'No message provided'}, status=400)

            system_prompt = {
                "role": "system",
                "content": (
                    "You are a medical assistant specialized in brain health and tumor diagnosis. "
                    "Provide detailed, informative responses that include explanations and context. "
                    "Focus on being educational while maintaining medical accuracy. "
                    "Include relevant medical terms but explain them in simple language. "
                    "Always remind users to consult healthcare professionals for medical advice."
                )
            }

            chat_history = [system_prompt, {"role": "user", "content": user_message}]

            # Ensure the correct API URL is being used
            response = client.chat.completions.create(
                model="llama3-70b-8192",  # Check if this is a valid model
                messages=chat_history,
                max_tokens=150,
                temperature=1.2
            )

            assistant_message = response.choices[0].message.content
            return JsonResponse({'reply': assistant_message})
        except Exception as e:
            print(f"Error with Groq API: {e}")
            return JsonResponse({'error': 'Something went wrong with the Groq API. Please try again later.'},
                                status=500)

    return JsonResponse({'error': 'Invalid request'}, status=400)

# Login View
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')  # Redirect to home after login
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})


def mask_email(email):
    """Mask email like t*****@gmail.com"""
    if "@" in email:
        username, domain = email.split("@")
        return username[0] + "*****@" + domain
    return email

@login_required
def profile_view(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('profile')

    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)

    # Masked email
    masked_email = mask_email(request.user.email)

    # Load profile picture OR default avatar
    if request.user.profile.profile_picture:
        profile_picture = static('images/default-avatar.jpg')
    else:
        profile_picture = static('images/default-avatar.jpg')  # Use static path

    return render(request, 'profile.html', {
        'user_form': user_form,
        'profile_form': profile_form,
        'masked_email': masked_email,
        'profile_picture': profile_picture
    }
                  )

@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Keeps user logged in
            messages.success(request, "Your password was successfully updated!")
            return redirect('profile')
    else:
        form = PasswordChangeForm(request.user)

    return render(request, 'change_password.html', {'form': form})

# Logout View
def logout_view(request):
    logout(request)
    return redirect('home')  # Redirect to home page after logout


def blog_view(request):
    return render(request, 'blog.html')


@login_required

def upload_mri(request):
    # Ensure doctor instance exists first
    try:
        doctor = request.user.doctor
    except Doctor.DoesNotExist:
        messages.warning(request, "Doctor profile not found. Please contact admin.")
        return render(request, 'upload_mri.html', {"form": None, "scans": [], "error": "Doctor profile not found."})

    # If doctor is not verified, prevent actions but do not redirect
    if not doctor.is_verified:
        messages.warning(request, "You need to be verified by an admin before uploading or filtering scans. Please upload your certificate first.")
        return render(request, 'upload_mri.html', {"form": None, "scans": [], "unverified": True})

    scans = MRI_Scan.objects.filter(doctor=doctor).order_by('-uploaded_at')

    # Handle filtering (only for verified users)
    time_range = request.GET.get("time_range")
    status = request.GET.get("status")
    patient_id = request.GET.get("patient_id")

    if patient_id:
        scans = scans.filter(patient_uid__icontains=patient_id)

    if status and status != "all":
        scans = scans.filter(status=status)  # Ensure 'status' field exists on MRI_Scan

    if time_range and time_range.isdigit():
        from datetime import timedelta, datetime
        cutoff = datetime.now() - timedelta(days=int(time_range))
        scans = scans.filter(uploaded_at__gte=cutoff)

    # Upload form logic
    if request.method == 'POST':
        form = MRIScanForm(request.POST, request.FILES)
        if form.is_valid():
            scan = form.save(commit=False)
            scan.doctor = doctor
            scan.save()
            return redirect('scan_detail', scan_id=scan.id)
    else:
        form = MRIScanForm()

    context = {
        'form': form,
        'scans': scans,
        'request': request  # pass request for template filtering persistence
    }
    return render(request, 'upload_mri.html', context)