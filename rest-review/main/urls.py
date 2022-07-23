from django.urls import path
from . import views  #importing our view file 

urlpatterns = [
    path("", views.homepage, name="home"), # mapping the homepage function
    path("add_rest", views.get_rest, name = "add_rest"), 
]

