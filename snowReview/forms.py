from django.forms import ModelForm
from .models import Snowboard, Terrain, Comment, Review, Size
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django import forms

class SnowboardForm(ModelForm):
    terrain = forms.MultipleChoiceField(choices=Terrain.TERRAIN_CHOICES, required=True, widget=forms.CheckboxSelectMultiple())
    profile = forms.ChoiceField(choices=Snowboard.PROFILES, required=True)
    rider = forms.ChoiceField(choices=Snowboard.SKILL, required=True, widget=forms.Select(attrs={'class': 'form-control'}))
    sizes = forms.MultipleChoiceField(choices=[(i, i) for i in range(120, 191)], widget=forms.CheckboxSelectMultiple())

    class Meta:
        model = Snowboard
        fields =  ('name', 'season', 'terrain', 'profile', 'rider', 'sizes', 'desc',)
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'season': forms.NumberInput(attrs={'class': 'form-control', 'min': 1900, 'max': 2099}),
            'desc': forms.Textarea(attrs={'class': 'form-control'}),
            'flex': forms.NumberInput(attrs={'class': 'form-control', 'min': 0, 'max': 10}),
        }
    
    def clean_terrain(self):
        terrain = self.cleaned_data.get('terrain')
        return Terrain.objects.filter(name__in=terrain)

    def clean_sizes(self):
        sizes = self.cleaned_data.get('sizes')
        return Size.objects.filter(size__in=sizes)   
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
    comment_text = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Leave a comment here', 'id': 'floatingTextarea'})
    )

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
            'riderHeight': forms.NumberInput(attrs={'min': 0, 'max': 10, 'step': '0.01'}),
            'riderWeight': forms.NumberInput(attrs={'min': 000, 'max': 500}),
        }