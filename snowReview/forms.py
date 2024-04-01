from django.forms import ModelForm
from .models import Snowboard, Terrain, Comment, Review
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
    rider = forms.ChoiceField(choices=Snowboard.SKILL, required=False)
    terrain = forms.MultipleChoiceField(choices=Terrain.TERRAIN_CHOICES, required=False)
    shape = forms.ChoiceField(choices=Snowboard.SHAPES, required=False)  # Changed 'SHAPE_CHOICES' to 'Snowboard.SHAPES'
    profile = forms.ChoiceField(choices=Snowboard.PROFILES, required=False)  # Changed 'PROFILE_CHOICES' to 'Snowboard.PROFILES'

class CustomAuthenticationForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ('username', 'password')

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['comment_text']

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['boardSize', 'date', 'conditions', 'snow24', 'snow7', 'riderHeight', 'riderWeight']
        labels = {
        'snow24': 'Snowfall in the last 24 hours (inches)',
        'snow7': 'Snowfall in the last 7 days (inches)',
        'riderHeight': 'Rider Height (Inches)',
        'riderWeight': 'Rider Weight (lbs)',
        'boardSize': 'Board Size (cm)',}
        # input sanitization
        # For pop up calender
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'snow24': forms.NumberInput(attrs={'min': 0, 'max': 100}),
            'snow7': forms.NumberInput(attrs={'min': 0, 'max': 200}),
            'riderHeight': forms.NumberInput(attrs={'min': 000, 'max':10}),
            'riderWeight': forms.NumberInput(attrs={'min': 000, 'max': 500}),
        }