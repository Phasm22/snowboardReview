from django.forms import ModelForm
from django.core.validators import MinValueValidator, MaxValueValidator, DecimalValidator
from .models import Snowboard, Terrain, Comment, Review, Size
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.models import User
from django import forms

# Form to add snowboard
class SnowboardForm(ModelForm):
    # Checkbox for terrain
    terrain = forms.MultipleChoiceField(choices=Terrain.TERRAIN_CHOICES, required=True, widget=forms.CheckboxSelectMultiple())
    profile = forms.ChoiceField(choices=Snowboard.PROFILES, required=True)

    # Add the pretty form class
    rider = forms.ChoiceField(choices=Snowboard.SKILL, required=True, widget=forms.Select(attrs={'class': 'form-control'}))

    # Checkbox grid for sizes
    sizes = forms.MultipleChoiceField(choices=[(i, i) for i in range(120, 191)], widget=forms.CheckboxSelectMultiple())
    
    # Add the pretty form class
    desc = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control'}), label='Description')

    # Option to add a pictrue
    image = forms.ImageField(required=False)

    class Meta:
        model = Snowboard
        fields =  ('name', 'season', 'image', 'terrain', 'profile', 'rider', 'sizes', 'desc',)
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'season': forms.NumberInput(attrs={'class': 'form-control', 'min': 1900, 'max': 2099}),
            'flex': forms.NumberInput(attrs={'class': 'form-control', 'min': 0, 'max': 10}),
        }
    
    # clean (validate and normalize) the data 
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
    # none are required to show a empty filter
    rider = forms.ChoiceField(choices=Snowboard.SKILL, required=False)
    terrain = forms.MultipleChoiceField(choices=Terrain.TERRAIN_CHOICES, required=False)
    shape = forms.ChoiceField(choices=Snowboard.SHAPES, required=False)
    profile = forms.ChoiceField(choices=Snowboard.PROFILES, required=False)

class CustomAuthenticationForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ('username', 'password')
class CommentForm(forms.ModelForm):
    # Define a form field 'comment_text'
    comment_text = forms.CharField(
        # Use a Textarea widget for the field
        widget=forms.Textarea(
            attrs={
                'class': 'form-control',  # Set the CSS class to 'form-control'
                'placeholder': 'Leave a comment here',  # Set the placeholder text
                'id': 'floatingTextarea'  # Set the id of the textarea
            }
        )
    )

    class Meta:
        model = Comment
        fields = ['comment_text']
        
class ReviewForm(forms.ModelForm):
    # set min and max snow24
    snow24 = forms.DecimalField(
        validators=[
            MinValueValidator(0),
            MaxValueValidator(100),
            DecimalValidator(max_digits=4, decimal_places=2)
        ]
    )

    # set min and max for snow7
    snow7 = forms.DecimalField(
        validators=[
            MinValueValidator(0),
            MaxValueValidator(200),
            DecimalValidator(max_digits=4, decimal_places=2)
        ]
    )
    class Meta:
        model = Review
        fields = ['boardSize', 'date', 'conditions', 'snow24', 'snow7', 'riderHeight', 'riderWeight']
        labels = {
            'snow24': 'Snowfall in the last 24 hours (inches)',
            'snow7': 'Snowfall in the last 7 days (inches)',
            'riderHeight': 'Rider Height (Inches)',
            'riderWeight': 'Rider Weight (lbs)',
            'boardSize': 'Board Size (cm)',
        }
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'riderHeight': forms.NumberInput(attrs={'min': 1, 'max': 300, 'step': '0.01'}),
            'riderWeight': forms.NumberInput(attrs={'min': 1, 'max': 500}),
        }