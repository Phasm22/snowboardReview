from django.forms import ModelForm
from django.core.validators import MinValueValidator, MaxValueValidator, DecimalValidator
from django.core.validators import MinValueValidator, MaxValueValidator, DecimalValidator
from .models import Snowboard, Terrain, Comment, Review, Size
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.models import User
from django import forms

# Form to add snowboard
class SnowboardForm(ModelForm):
    """
    A Django form for creating and updating Snowboard instances.

    This form is a ModelForm for the Snowboard model. It includes MultipleChoiceFields for 
    terrain and sizes, ChoiceFields for profile and rider skill, a CharField for description, 
    and an ImageField for the snowboard image. The 'terrain', 'profile', 'rider', and 'sizes' 
    fields use custom widgets, and the 'rider' and 'desc' fields use the 'form-control' CSS class.

    The Meta class specifies the model, fields, and widgets to use for this form. The 'name', 
    'season', and 'flex' fields use the 'form-control' CSS class, and the 'season' and 'flex' 
    fields have min and max attributes.

    The 'clean_terrain' and 'clean_sizes' methods are used to validate and normalize the 'terrain' 
    and 'sizes' fields, respectively.

    Attributes:
        terrain (forms.MultipleChoiceField): The types of terrain the snowboard is suitable for.
        profile (forms.ChoiceField): The profile of the snowboard.
        rider (forms.ChoiceField): The skill level of the rider.
        sizes (forms.MultipleChoiceField): The available sizes of the snowboard.
        desc (forms.CharField): The description of the snowboard.
        image (forms.ImageField): The image of the snowboard.
    """
    
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
    """
    A Django form for filtering snowboards based on rider skill, terrain, shape, and profile.

    This form includes ChoiceFields for rider skill, snowboard shape, and snowboard profile, 
    and a MultipleChoiceField for terrain. None of the fields are required, allowing for an 
    empty filter.

    Attributes:
        rider (forms.ChoiceField): The skill level of the rider.
        terrain (forms.MultipleChoiceField): The types of terrain the snowboard is suitable for.
        shape (forms.ChoiceField): The shape of the snowboard.
        profile (forms.ChoiceField): The profile of the snowboard.
    """

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
    """
    A Django form for creating and updating Review instances.

    This form is a ModelForm for the Review model. It includes fields for board size, date, 
    conditions, snowfall in the last 24 hours and 7 days, rider height, and rider weight.

    The snow24 and snow7 fields are DecimalFields with custom validators to ensure the entered 
    values are within a specific range and have a specific number of digits and decimal places.

    The Meta class specifies the model, fields, labels, and widgets to use for this form. The date 
    field uses a DateInput widget with a 'date' type, and the riderHeight and riderWeight fields 
    use NumberInput widgets with min and max attributes.

    Attributes:
        snow24 (forms.DecimalField): Snowfall in the last 24 hours (in inches).
        snow7 (forms.DecimalField): Snowfall in the last 7 days (in inches).
    """

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
    """
    A Django form for creating and updating Review instances.

    This form is a ModelForm for the Review model. It includes fields for board size, date, 
    conditions, snowfall in the last 24 hours and 7 days, rider height, and rider weight.

    The snow24 and snow7 fields are DecimalFields with custom validators to ensure the entered 
    values are within a specific range and have a specific number of digits and decimal places.

    The Meta class specifies the model, fields, labels, and widgets to use for this form. The date 
    field uses a DateInput widget with a 'date' type, and the riderHeight and riderWeight fields 
    use NumberInput widgets with min and max attributes.

    Attributes:
        snow24 (forms.DecimalField): Snowfall in the last 24 hours (in inches).
        snow7 (forms.DecimalField): Snowfall in the last 7 days (in inches).
    """
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