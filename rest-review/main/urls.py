from django.urls import path
from . import views  #importing our view file 

urlpatterns = [
    path("", views.homepage, name="home"), # mapping the homepage function
    path("add-rest", views.add_rest, name = "add-rest"),
    path("my-rests", views.show_rest, name = "my-rests"), 
]

