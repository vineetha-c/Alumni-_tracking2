from django.db import models
from django.contrib.auth.models import User

class GraduationYear(models.Model):
    year = models.PositiveIntegerField(unique=True)

    class Meta:
        ordering = ["-year"]

    def __str__(self):
        return str(self.year)


class Department(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class AlumniProfile(models.Model):
    EMPLOYMENT_CHOICES = [
        ("employed", "Employed"),
        ("student", "Higher Studies"),
        ("entrepreneur", "Entrepreneur"),
        ("seeking", "Seeking Opportunities"),
        ("other", "Other"),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="alumni_profile")
    full_name = models.CharField(max_length=150)
    photo = models.ImageField(upload_to="profiles/", blank=True, null=True)
    graduation_year = models.ForeignKey(GraduationYear, on_delete=models.SET_NULL, null=True, blank=True)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True)
    current_company = models.CharField(max_length=150, blank=True)
    current_role = models.CharField(max_length=150, blank=True)
    employment_status = models.CharField(max_length=20, choices=EMPLOYMENT_CHOICES, default="employed")
    city = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=100, blank=True)
    linkedin_url = models.URLField(blank=True)
    github_url = models.URLField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    bio = models.TextField(blank=True)
    skills = models.CharField(max_length=255, blank=True, help_text="Comma-separated skills")
    available_for_mentoring = models.BooleanField(default=False)
    is_public = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["full_name"]

    def __str__(self):
        return self.full_name


class ContactMessage(models.Model):
    name = models.CharField(max_length=120)
    email = models.EmailField()
    subject = models.CharField(max_length=150)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name} - {self.subject}"