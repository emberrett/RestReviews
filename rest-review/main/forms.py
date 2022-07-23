from django.forms import ModelForm
from main.models import Rest

class AddRest(ModelForm):
    class Meta:
        exclude = ["user"]
        model = Rest
        fields = ["user",
                "restaraunt",
                "rating",
                "category",
                "street_address",
                "city",
                "state",
                "postal_code",
                "drive_time",
                "notes"
            ]