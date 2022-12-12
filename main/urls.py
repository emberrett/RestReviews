from django.urls import path
from . import views  # importing our view file

urlpatterns = [
    path("", views.homepage, name="home"),  # mapping the homepage function
    path("add-rest", views.add_rest, name="add-rest"),
    path("edit-rest/<int:id>/", views.edit_rest, name='edit-rest'),
    path("edit-rest", views.edit_rest),
    path("my-rests", views.show_rest, name="my-rests"),
    path('delete-rest/<int:id>', views.delete_rest, name='delete-rest'),
]
