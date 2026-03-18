from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("about/", views.about, name="about"),
    path("register/", views.register, name="register"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("profile/", views.profile_detail, name="profile_detail"),
    path("profile/edit/", views.profile_edit, name="profile_edit"),
    path("alumni/", views.alumni_list, name="alumni_list"),
    path("alumni/<int:pk>/", views.alumni_detail, name="alumni_detail"),
    path("contact/", views.contact, name="contact"),
    path("success/", views.success, name="success"),
]