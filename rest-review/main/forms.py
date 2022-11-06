from django.forms import ModelForm
from main.models import Rest
from django.shortcuts import get_object_or_404
from django.shortcuts import render


class AddRest(ModelForm):
    class Meta:
        exclude = ["id", "user", "address", "rest","rating", "latitude", "longitude"]
        model = Rest
