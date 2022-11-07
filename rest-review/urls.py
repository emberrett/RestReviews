from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", include("main.urls")),  # add this line
    path("accounts/",include("accounts.urls")),
    path("accounts/password/",include("accounts.urls"))
]