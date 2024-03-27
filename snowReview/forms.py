from django.forms import ModelForm
from .models import Snowboard
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class SnowboardForm(ModelForm):
    class Meta:
        model = Snowboard
        fields =  ('name', 'desc',)