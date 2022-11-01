from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.models import auth
from accounts.forms import RegisterUser
from django.urls import reverse_lazy
from django.views import generic

class SignUpView(generic.CreateView):
    form_class = RegisterUser
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"

