from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail, BadHeaderError
from django.core.validators import validate_email
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib import messages
from django.core.exceptions import ValidationError
from django_ratelimit.decorators import ratelimit
from django.db.models import Sum, Count, Q, Avg
from django.utils import timezone
from datetime import datetime, timedelta, date
from decimal import Decimal
import anthropic
import os
from .tokens import email_verification_token, password_reset_token
from .models import WorkerProfile, ShiftLog, AdvanceRequest



def index(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    return render(request, 'index.html')

@login_required
def dashboard(request):
    return render(request, 'dashboard.html')

# ─────────────────────────────────────────────
# REGISTER
# ─────────────────────────────────────────────
@ratelimit(key='ip', rate='5/m', block=True)
def register(request):
    if request.method == 'POST':
        full_name = request.POST.get('full_name', '').strip()
        email = request.POST.get('email', '').strip().lower()
        phone_number = request.POST.get('phone_number', '').strip()
        job_type = request.POST.get('job_type', '').strip()
        daily_avg_earnings = request.POST.get('daily_avg_earnings', '').strip()
        password = request.POST.get('password', '').strip()
        password2 = request.POST.get('confirm_password', '').strip()

        # Validation
        if not full_name:
            messages.error(request, "Full name is required.")
            return render(request, 'register.html')

        if not email:
            messages.error(request, "Email address is required.")
            return render(request, 'register.html')

        if not phone_number:
            messages.error(request, "Phone number is required.")
            return render(request, 'register.html')

        if not job_type:
            messages.error(request, "Job type is required.")
            return render(request, 'register.html')

        if not daily_avg_earnings:
            messages.error(request, "Daily average earnings is required.")
            return render(request, 'register.html')

        if not password or not password2:
            messages.error(request, "Please fill in both password fields.")
            return render(request, 'register.html')

        try:
            validate_email(email)
        except ValidationError:
            messages.error(request, "Please enter a valid email address.")
            return render(request, 'register.html')

        if len(password) < 8:
            messages.error(request, "Password must be at least 8 characters.")
            return render(request, 'register.html')

        if password != password2:
            messages.error(request, "Passwords do not match.")
            return render(request, 'register.html')

        if User.objects.filter(email=email).exists():
            messages.error(request, "An account with that email already exists.")
            return render(request, 'register.html')

        # Split full name
        name_parts = full_name.split()
        first_name = name_parts[0] if name_parts else ''
        last_name = ' '.join(name_parts[1:]) if len(name_parts) > 1 else ''

        # Username generation
        base_username = f"{first_name}_{last_name}".lower().replace(' ', '_')
        username = base_username
        counter = 1
        while User.objects.filter(username=username).exists():
            username = f"{base_username}{counter}"
            counter += 1

        # Create user
        user = User.objects.create(
            username=username,
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=make_password(password),
            is_active=True,
        )

        # Create WorkerProfile
        WorkerProfile.objects.create(
            user=user,
            job_type=job_type,
            phone_number=phone_number,
            daily_avg_earnings=Decimal(daily_avg_earnings),
        )

        messages.success(request, "Account created successfully! Please sign in.")
        return redirect('login')

    return render(request, 'register.html')


# ─────────────────────────────────────────────
# EMAIL VERIFICATION
# ─────────────────────────────────────────────
def verify_email(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except Exception:
        return render(request, 'verify_result.html', {
            'status': 'invalid',
            'heading': 'Invalid link',
            'message': 'Verification link is invalid.',
        })

    if email_verification_token.check_token(user, token):
        user.is_active = True
        user.is_email_verified = True
        user.save()

        return render(request, 'verify_result.html', {
            'status': 'success',
            'heading': 'Email verified',
            'message': 'Your account is now active.',
        })

    return render(request, 'verify_result.html', {
        'status': 'expired',
        'heading': 'Link expired',
        'message': 'Verification link expired.',
    })
    
# ─────────────────────────────────────────────
#  LOGIN  (email + password)
# ─────────────────────────────────────────────

@ratelimit(key='ip', rate='10/m', block=True)
def login(request):
    # Already authenticated — skip the login page
    if request.user.is_authenticated:
        return redirect('dashboard')
 
    if request.method == 'POST':
        email    = request.POST.get('email', '').strip().lower()
        password = request.POST.get('password', '').strip()
 
        # Both fields required
        if not email or not password:
            messages.error(request, "Please enter your email and password.")
            return render(request, 'login.html')
 
        # Find user by email
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            messages.error(request, "No account found with that email address.")
            return render(request, 'login.html')
 
        # Wrong password
        if not user.check_password(password):
            messages.error(request, "Incorrect password. Please try again.")
            return render(request, 'login.html')
 
        # Success — create session
        auth_login(request, user, backend='django.contrib.auth.backends.ModelBackend')
        return redirect('dashboard')
 
    return render(request, 'login.html')
 
 

# ─────────────────────────────────────────────
# RESEND VERIFICATION
# ─────────────────────────────────────────────
def resend_verification(request):
    if request.method != 'POST':
        return redirect('register')

    email = request.POST.get('email', '').strip().lower()

    try:
        user = User.objects.get(email=email, is_active=False)
    except User.DoesNotExist:
        return render(request, 'verify_pending.html', {'email': email})

    try:
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = email_verification_token.make_token(user)
        domain = get_current_site(request).domain

        verification_link = f"http://{domain}/verify-email/{uid}/{token}/"

        send_mail(
            "Verify your DjangoPilot account",
            f"Click here to verify:\n{verification_link}",
            "noreply@djangopilot.com",
            [email],
            fail_silently=False,
        )

    except Exception:
        messages.error(request, "Could not resend email.")
        return render(request, 'verify_pending.html', {'email': email})

    return render(request, 'verify_pending.html', {'email': email, 'resent': True})

def logout(request):
    auth.logout(request)
    return redirect('login')

def forgot_password(request):
    if request.method == "POST":
        email = request.POST.get("email", "").strip().lower()

        if not email:
            messages.error(request, "Please enter your email.")
            return render(request, "forgot_password.html")

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            messages.error(request, "No account found with that email.")
            return render(request, "forgot_password.html")

        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = password_reset_token.make_token(user)
        domain = get_current_site(request).domain

        reset_link = f"http://{domain}/reset-password/{uid}/{token}/"

        send_mail(
            "Reset your DjangoPilot password",
            f"Click the link below to reset your password:\n\n{reset_link}",
            "noreply@djangopilot.com",
            [email],
            fail_silently=False,
        )

        return render(request, "reset_email_sent.html", {"email": email})

    return render(request, "forgot_password.html")

def reset_password(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except Exception:
        return render(request, "reset_result.html", {
            "status": "invalid",
            "message": "Invalid reset link."
        })

    if not password_reset_token.check_token(user, token):
        return render(request, "reset_result.html", {
            "status": "expired",
            "message": "Reset link expired."
        })

    if request.method == "POST":
        password = request.POST.get("password", "").strip()
        confirm = request.POST.get("confirm_password", "").strip()

        if len(password) < 8:
            messages.error(request, "Password must be at least 8 characters.")
            return render(request, "reset_password.html")

        if password != confirm:
            messages.error(request, "Passwords do not match.")
            return render(request, "reset_password.html")

        user.password = make_password(password)
        user.save()

        return render(request, "reset_result.html", {
            "status": "success",
            "message": "Your password has been reset successfully."
        })

    return render(request, "reset_password.html")


@login_required(login_url='/login/')
def dashboard(request):
    worker = request.user
    try:
        profile = worker.worker_profile
    except WorkerProfile.DoesNotExist:
        profile = WorkerProfile.objects.create(user=worker)
    
    # Get this month's shifts and earnings
    from datetime import date
    today = date.today()
    first_day = today.replace(day=1)
    
    shifts_this_month = ShiftLog.objects.filter(
        worker=worker,
        date__gte=first_day
    ).count()
    
    earnings_this_month = ShiftLog.objects.filter(
        worker=worker,
        date__gte=first_day
    ).aggregate(total=Sum('earnings_today'))['total'] or Decimal('0')
    
    # Get recent shifts (last 7 days)
    seven_days_ago = today - timedelta(days=7)
    recent_shifts = ShiftLog.objects.filter(
        worker=worker,
        date__gte=seven_days_ago
    ).order_by('-date')
    
    total_hours = recent_shifts.aggregate(total=Sum('hours_worked'))['total'] or Decimal('0')
    total_earnings = recent_shifts.aggregate(total=Sum('earnings_today'))['total'] or Decimal('0')
    
    # Get recent advances
    recent_advances = AdvanceRequest.objects.filter(
        worker=worker
    ).order_by('-requested_at')[:5]
    
    # Calculate shifts needed for eligibility
    shifts_needed = max(0, 5 - profile.total_shifts_logged)
    
    context = {
        'shifts_this_month': shifts_this_month,
        'earnings_this_month': earnings_this_month,
        'trust_score': profile.trust_score,
        'is_eligible': profile.is_eligible,
        'max_advance_amount': profile.max_advance_amount,
        'total_shifts_logged': profile.total_shifts_logged,
        'shifts_needed': shifts_needed,
        'recent_shifts': recent_shifts,
        'total_hours': total_hours,
        'total_earnings': total_earnings,
        'recent_advances': recent_advances,
    }
    
    return render(request, "dashboard.html", context)

@login_required(login_url='/login/')
def log_shift(request):
    if request.method == 'POST':
        hours_worked = request.POST.get('hours_worked')
        earnings_today = request.POST.get('earnings_today')
        job_description = request.POST.get('job_description')
        
        try:
            hours_worked = Decimal(hours_worked)
            earnings_today = Decimal(earnings_today)
        except (ValueError, TypeError):
            messages.error(request, "Please enter valid numbers for hours and earnings.")
            return redirect('dashboard')
        
        # Create shift log
        ShiftLog.objects.create(
            worker=request.user,
            date=date.today(),
            hours_worked=hours_worked,
            earnings_today=earnings_today,
            job_description=job_description
        )
        
        # Update worker profile
        profile = request.user.worker_profile
        profile.total_shifts_logged += 1
        
        # Calculate trust score
        calculate_trust_score(profile)
        
        messages.success(request, "Shift logged successfully!")
        return redirect('dashboard')
    
    return redirect('dashboard')

def calculate_trust_score(profile):
    """Calculate trust score based on shift patterns"""
    worker = profile.user
    shifts = ShiftLog.objects.filter(worker=worker).order_by('-date')
    
    if shifts.count() < 2:
        profile.trust_score = 20
        profile.save()
        return
    
    score = 50  # Base score
    
    # Consistency bonus: logged shifts 3 days in a row
    recent_shifts = shifts[:7]
    dates = [shift.date for shift in recent_shifts]
    consecutive = 0
    for i in range(len(dates) - 1):
        if (dates[i] - dates[i + 1]).days == 1:
            consecutive += 1
        else:
            break
    if consecutive >= 2:
        score += 10
    
    # Earnings stability: if today's earnings within 30% of daily average
    if shifts.count() >= 3:
        avg_earnings = shifts.aggregate(avg=Avg('earnings_today'))['avg'] or profile.daily_avg_earnings
        latest = shifts.first()
        if avg_earnings > 0:
            diff = abs(latest.earnings_today - avg_earnings) / avg_earnings
            if diff <= 0.3:
                score += 5
    
    # Volume bonus: if earnings today > daily average
    if shifts.count() >= 1:
        latest = shifts.first()
        if latest.earnings_today > profile.daily_avg_earnings:
            score += 5
    
    # Penalty: gap of more than 2 days with no log
    if shifts.count() >= 2:
        latest = shifts.first()
        second_latest = shifts[1]
        gap = (latest.date - second_latest.date).days
        if gap > 2:
            score -= 10
    
    # Cap score at 100
    score = min(score, 100)
    profile.trust_score = score
    
    # Update eligibility and max advance amount
    if score >= 60 and profile.total_shifts_logged >= 5:
        profile.is_eligible = True
        # Calculate max advance: 50% of last 7 days earnings
        seven_days_ago = date.today() - timedelta(days=7)
        last_7_earnings = ShiftLog.objects.filter(
            worker=worker,
            date__gte=seven_days_ago
        ).aggregate(total=Sum('earnings_today'))['total'] or Decimal('0')
        profile.max_advance_amount = last_7_earnings * Decimal('0.5')
    else:
        profile.is_eligible = False
        profile.max_advance_amount = Decimal('0')
    
    profile.save()

@login_required(login_url='/login/')
def advance_request(request):
    profile = request.user.worker_profile
    
    if request.method == 'POST':
        amount_requested = request.POST.get('amount_requested')
        
        try:
            amount_requested = Decimal(amount_requested)
        except (ValueError, TypeError):
            messages.error(request, "Please enter a valid amount.")
            return render(request, 'advance_request.html', {'max_advance_amount': profile.max_advance_amount})
        
        if not profile.is_eligible:
            messages.error(request, "You are not eligible for an advance yet.")
            return redirect('dashboard')
        
        if amount_requested > profile.max_advance_amount:
            messages.error(request, f"You can only request up to ₦{profile.max_advance_amount}")
            return render(request, 'advance_request.html', {'max_advance_amount': profile.max_advance_amount})
        
        # Get last 7 days earnings for AI decision
        seven_days_ago = date.today() - timedelta(days=7)
        last_7_earnings = ShiftLog.objects.filter(
            worker=request.user,
            date__gte=seven_days_ago
        ).aggregate(total=Sum('earnings_today'))['total'] or Decimal('0')
        
        # Create advance request with pending status
        advance = AdvanceRequest.objects.create(
            worker=request.user,
            amount_requested=amount_requested,
            status='pending',
            ai_decision_reason='Processing...'
        )
        
        # Call AI for decision (simplified for demo - auto-approve if within limits)
        if amount_requested <= profile.max_advance_amount:
            advance.status = 'approved'
            advance.amount_approved = amount_requested
            advance.ai_decision_reason = f"Based on your consistent work history and trust score of {profile.trust_score}, you qualify for this advance. Keep up the great work!"
        else:
            advance.status = 'rejected'
            advance.ai_decision_reason = f"Requested amount exceeds your maximum eligible amount of ₦{profile.max_advance_amount}."
        
        advance.save()
        
        if advance.status == 'approved':
            messages.success(request, f"Advance approved! ₦{amount_requested} will be processed.")
        else:
            messages.error(request, f"Advance request rejected: {advance.ai_decision_reason}")
        
        return redirect('dashboard')
    
    return render(request, 'advance_request.html', {'max_advance_amount': profile.max_advance_amount})
