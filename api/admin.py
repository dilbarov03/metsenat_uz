from django.contrib import admin

from .models import Funding, Sponsor, Student, University

@admin.register(Sponsor)
class SponsorAdmin(admin.ModelAdmin):
    list_display = ["full_name", "phone", "summa", "status"]

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ["full_name", "student_type", "university", "contract_amount"]

@admin.register(Funding)
class FundingAdmin(admin.ModelAdmin):
    list_display = ["sponsor", "student", "amount"]

@admin.register(University)
class UniversityAdmin(admin.ModelAdmin):
    list_display = ["name"]