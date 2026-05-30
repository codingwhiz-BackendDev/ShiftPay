from django.contrib import admin
from .models import WorkerProfile, ShiftLog, AdvanceRequest

@admin.register(WorkerProfile)
class WorkerProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'job_type', 'phone_number', 'daily_avg_earnings', 'trust_score', 'is_eligible', 'max_advance_amount', 'created_at']
    list_filter = ['job_type', 'is_eligible', 'created_at']
    search_fields = ['user__email', 'user__first_name', 'user__last_name', 'phone_number']
    readonly_fields = ['created_at']

@admin.register(ShiftLog)
class ShiftLogAdmin(admin.ModelAdmin):
    list_display = ['worker', 'date', 'hours_worked', 'earnings_today', 'job_description', 'created_at']
    list_filter = ['date', 'created_at']
    search_fields = ['worker__email', 'worker__first_name', 'job_description']
    readonly_fields = ['created_at']
    date_hierarchy = 'date'

@admin.register(AdvanceRequest)
class AdvanceRequestAdmin(admin.ModelAdmin):
    list_display = ['worker', 'amount_requested', 'amount_approved', 'status', 'ai_decision_reason', 'requested_at', 'repaid_at']
    list_filter = ['status', 'requested_at', 'repaid_at']
    search_fields = ['worker__email', 'worker__first_name', 'ai_decision_reason']
    readonly_fields = ['requested_at', 'repaid_at']
    date_hierarchy = 'requested_at'
