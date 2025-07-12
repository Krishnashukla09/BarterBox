from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q

from .models import UserProfile, SwapRequest
from .forms import SignupForm, SwapRequestForm, ProfileForm


@login_required
def dashboard(request):
    return render(request, 'core/dashboard.html')

def landing_page(request):
    return render(request, 'core/index.html')

@login_required
def browse_users(request):
    query = request.GET.get('skill')
    availability = request.GET.get('availability')

    users = UserProfile.objects.filter(is_public=True).exclude(user=request.user)

    if availability:
        users = users.filter(availability__iexact=availability)

    if query:
        users = users.filter(
            Q(skills_offered__name__icontains=query) |
            Q(skills_wanted__name__icontains=query)
        ).distinct()

    return render(request, 'core/browse.html', {'users': users})


def signup_view(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()

            profile = UserProfile.objects.create(
                user=user,
                location=form.cleaned_data['location'],
                availability=form.cleaned_data['availability'],
                is_public=form.cleaned_data['is_public'],
            )
            profile.skills_offered.set(form.cleaned_data['skills_offered'])
            profile.skills_wanted.set(form.cleaned_data['skills_wanted'])
            profile.save()

            login(request, user)  # Auto-login after signup
            return redirect('dashboard')
    else:
        form = SignupForm()
    return render(request, 'core/signup.html', {'form': form})


@login_required
def browse_users(request):
    users = UserProfile.objects.filter(is_public=True).exclude(user=request.user)
    return render(request, 'core/browse.html', {'users': users})


@login_required
def send_swap_request(request, user_id):
    receiver = get_object_or_404(User, pk=user_id)
    
    if request.method == 'POST':
        form = SwapRequestForm(request.POST)
        if form.is_valid():
            swap = form.save(commit=False)
            swap.sender = request.user
            swap.receiver = receiver
            swap.save()
            return redirect('dashboard')
    else:
        form = SwapRequestForm()
    
    return render(request, 'core/swap_form.html', {
        'form': form,
        'receiver': receiver,
    })


@login_required
def swap_requests_dashboard(request):
    sent = SwapRequest.objects.filter(sender=request.user)
    received = SwapRequest.objects.filter(receiver=request.user)

    if request.method == 'POST':
        request_id = request.POST.get('request_id')
        action = request.POST.get('action')
        swap = get_object_or_404(SwapRequest, id=request_id, receiver=request.user)
        
        if action == 'accept':
            swap.status = 'accepted'
        elif action == 'reject':
            swap.status = 'rejected'
        swap.save()
        return redirect('swap_requests')

    return render(request, 'core/swap_dashboard.html', {
        'sent_requests': sent,
        'received_requests': received,
    })


@login_required
def profile_view(request):
    # ✅ Automatically create profile if it doesn't exist
    profile, created = UserProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = ProfileForm(instance=profile)

    return render(request, 'core/profile.html', {'form': form, 'profile': profile})


@login_required
def home(request):
    query = request.GET.get('skill')
    availability = request.GET.get('availability')

    users = UserProfile.objects.filter(is_public=True).exclude(user=request.user)

    if availability:
        users = users.filter(availability__iexact=availability)

    if query:
        users = users.filter(
            Q(skills_offered__name__icontains=query) | Q(skills_wanted__name__icontains=query)
        ).distinct()

    return render(request, 'core/home.html', {'users': users})
