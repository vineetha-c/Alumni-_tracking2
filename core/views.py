from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .forms import UserRegisterForm, AlumniProfileForm, ContactForm
from .models import AlumniProfile, Department, GraduationYear

def home(request):
    total_alumni = AlumniProfile.objects.filter(is_public=True).count()
    mentors = AlumniProfile.objects.filter(is_public=True, available_for_mentoring=True).count()
    departments = Department.objects.count()
    years = GraduationYear.objects.count()

    featured_alumni = AlumniProfile.objects.filter(is_public=True)[:6]

    context = {
        "total_alumni": total_alumni,
        "mentors": mentors,
        "departments": departments,
        "years": years,
        "featured_alumni": featured_alumni,
    }
    return render(request, "core/home.html", context)


def about(request):
    return render(request, "core/about.html")


def register(request):
    if request.user.is_authenticated:
        return redirect("dashboard")

    if request.method == "POST":
        user_form = UserRegisterForm(request.POST)
        profile_form = AlumniProfileForm(request.POST, request.FILES)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save(commit=False)
            user.email = user_form.cleaned_data["email"]
            user.first_name = user_form.cleaned_data["first_name"]
            user.last_name = user_form.cleaned_data["last_name"]
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user
            if not profile.full_name:
                profile.full_name = f"{user.first_name} {user.last_name}".strip() or user.username
            profile.save()

            login(request, user)
            messages.success(request, "Registration successful! Welcome to Alumni Connect.")
            return redirect("dashboard")
    else:
        user_form = UserRegisterForm()
        profile_form = AlumniProfileForm()

    return render(request, "core/register.html", {
        "user_form": user_form,
        "profile_form": profile_form
    })


@login_required
def dashboard(request):
    profile = getattr(request.user, "alumni_profile", None)
    recent_alumni = AlumniProfile.objects.filter(is_public=True).exclude(user=request.user)[:8]

    return render(request, "core/dashboard.html", {
        "profile": profile,
        "recent_alumni": recent_alumni
    })


@login_required
def profile_edit(request):
    profile = getattr(request.user, "alumni_profile", None)

    if not profile:
        messages.error(request, "Profile not found.")
        return redirect("dashboard")

    if request.method == "POST":
        form = AlumniProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully.")
            return redirect("profile_detail")
    else:
        form = AlumniProfileForm(instance=profile)

    return render(request, "core/profile_form.html", {"form": form})


@login_required
def profile_detail(request):
    profile = getattr(request.user, "alumni_profile", None)
    return render(request, "core/profile_detail.html", {"profile": profile})


def alumni_list(request):
    query = request.GET.get("q", "")
    department_id = request.GET.get("department", "")
    year_id = request.GET.get("year", "")
    mentoring = request.GET.get("mentoring", "")

    alumni = AlumniProfile.objects.filter(is_public=True)

    if query:
        alumni = alumni.filter(
            Q(full_name__icontains=query) |
            Q(current_company__icontains=query) |
            Q(current_role__icontains=query) |
            Q(city__icontains=query) |
            Q(country__icontains=query) |
            Q(skills__icontains=query)
        )

    if department_id:
        alumni = alumni.filter(department_id=department_id)

    if year_id:
        alumni = alumni.filter(graduation_year_id=year_id)

    if mentoring == "1":
        alumni = alumni.filter(available_for_mentoring=True)

    departments = Department.objects.all()
    years = GraduationYear.objects.all()

    return render(request, "core/alumni_list.html", {
        "alumni": alumni,
        "departments": departments,
        "years": years,
        "query": query,
        "department_id": department_id,
        "year_id": year_id,
        "mentoring": mentoring,
    })


def alumni_detail(request, pk):
    profile = get_object_or_404(AlumniProfile, pk=pk, is_public=True)
    return render(request, "core/alumni_detail.html", {"profile": profile})


def contact(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Message sent successfully!")
            return redirect("success")
    else:
        form = ContactForm()

    return render(request, "core/contact.html", {"form": form})


def success(request):
    return render(request, "core/success.html")