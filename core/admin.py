from django.contrib import admin
from .models import GraduationYear, Department, AlumniProfile, ContactMessage

@admin.register(GraduationYear)
class GraduationYearAdmin(admin.ModelAdmin):
    list_display = ("year",)
    search_fields = ("year",)


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(AlumniProfile)
class AlumniProfileAdmin(admin.ModelAdmin):
    list_display = (
        "full_name",
        "user",
        "department",
        "graduation_year",
        "current_company",
        "employment_status",
        "available_for_mentoring",
        "is_public",
    )
    list_filter = ("department", "graduation_year", "employment_status", "available_for_mentoring", "is_public")
    search_fields = ("full_name", "user__username", "current_company", "city", "country")


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "subject", "created_at")
    search_fields = ("name", "email", "subject")
    readonly_fields = ("created_at",)