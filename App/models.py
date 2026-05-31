from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class WorkerProfile(models.Model):
    JOB_TYPE_CHOICES = [
        ('uber_bolt', 'Uber/Bolt Driver'),
        ('bus_driver', 'Bus Driver'),
        ('market_trader', 'Market Trader'),
        ('artisan', 'Artisan/Technician'),
        ('delivery_rider', 'Delivery Rider'),
        ('other', 'Other'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='worker_profile')
    job_type = models.CharField(max_length=20, choices=JOB_TYPE_CHOICES)
    phone_number = models.CharField(max_length=15)
    daily_avg_earnings = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_shifts_logged = models.IntegerField(default=0)
    trust_score = models.IntegerField(default=0)
    is_eligible = models.BooleanField(default=False)
    max_advance_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    ai_insight = models.TextField(blank=True, null=True)
    last_insight_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.get_full_name()} - {self.get_job_type_display()}"

class ShiftLog(models.Model):
    worker = models.ForeignKey(User, on_delete=models.CASCADE, related_name='shift_logs')
    date = models.DateField()
    hours_worked = models.DecimalField(max_digits=5, decimal_places=2)
    earnings_today = models.DecimalField(max_digits=10, decimal_places=2)
    job_description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-date', '-created_at']
    
    def __str__(self):
        return f"{self.worker.get_full_name()} - {self.date} - ₦{self.earnings_today}"

class AdvanceRequest(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('repaid', 'Repaid'),
    ]
    
    PAYOUT_METHOD_CHOICES = [
        ('opay', 'OPay'),
        ('palmpay', 'PalmPay'),
        ('bank_transfer', 'Bank Transfer'),
        ('cash_agent', 'Cash Agent'),
    ]
    
    worker = models.ForeignKey(User, on_delete=models.CASCADE, related_name='advance_requests')
    amount_requested = models.DecimalField(max_digits=10, decimal_places=2)
    amount_approved = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    ai_decision_reason = models.TextField()
    payout_method = models.CharField(max_length=20, choices=PAYOUT_METHOD_CHOICES, default='opay')
    account_number = models.CharField(max_length=20, blank=True, null=True)
    requested_at = models.DateTimeField(auto_now_add=True)
    repaid_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-requested_at']
    
    def __str__(self):
        return f"{self.worker.get_full_name()} - ₦{self.amount_requested} - {self.status}"

class RepaymentSchedule(models.Model):
    advance = models.OneToOneField(AdvanceRequest, on_delete=models.CASCADE, related_name='repayment_schedule')
    total_repayment = models.DecimalField(max_digits=10, decimal_places=2)
    daily_deduction = models.DecimalField(max_digits=10, decimal_places=2)
    days_remaining = models.IntegerField(default=14)
    start_date = models.DateField()
    is_complete = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Repayment for {self.advance.worker.get_full_name()} - ₦{self.total_repayment}"
