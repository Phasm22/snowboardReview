from django.forms import ModelForm
from .models import Snowboard, Terrain
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django import forms

class SnowboardForm(ModelForm):
    class Meta:
        model = Snowboard
        fields =  ('name', 'desc',)

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email', 'password1', 'password2')

class GuideForm(forms.Form):
    skill = forms.ChoiceField(choices=Snowboard.SKILL, widget=forms.RadioSelect)
    # can select more than one shape
    shape = forms.ChoiceField(choices=Snowboard.SHAPES, widget=forms.RadioSelect)
    profile = forms.ChoiceField(choices=Snowboard.PROFILES)
    terrain = forms.MultipleChoiceField(choices=Terrain.TERRAIN_CHOICES, widget=forms.CheckboxSelectMultiple)

class CustomAuthenticationForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ('username', 'password')