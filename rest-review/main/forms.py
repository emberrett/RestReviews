from ast import Add
from django.forms import ModelForm
from main.models import Rest

class AddRest(ModelForm):
    def __init__(self, *args, **kwargs):
        self._user = kwargs.pop('user')
        super(AddRest, self).__init__(*args, **kwargs)

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
    def save(self, commit=True):
        inst = super(AddRest, self).save(commit=False)
        inst.user = self._user
        if commit:
            inst.save()
            self.save_m2m()
        return inst
