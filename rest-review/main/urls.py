from django.urls import path
from . import views  #importing our view file 

urlpatterns = [
    path("", views.homepage, name="home"), # mapping the homepage function
    path("add-çrest", views.get_rest, name = "add-rest"), 
]

