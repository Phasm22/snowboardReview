from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.views import generic
import logging
from django.core.validators import MinValueValidator, MaxValueValidator, DecimalValidator, MaxLengthValidator

# Create your models here.

# Review objects
class Review(models.Model):
    BOARD_SIZES = [(str(i), f"{i} cm") for i in range(130, 170)]

    snow24 = models.DecimalField(
    max_digits=4, 
    decimal_places=2, 
    validators=[
        MinValueValidator(0),
        MaxValueValidator(100)
        ]
    )
    snow7 = models.DecimalField(
        max_digits=4, 
        decimal_places=2, 
        validators=[
            MinValueValidator(0),
            MaxValueValidator(200)
        ]
    )
    
    boardSize = models.CharField(max_length=200, choices=BOARD_SIZES, default=BOARD_SIZES[0][0])
    date = models.DateField(default='2024-01-01')
    conditions = models.CharField(max_length=200, default='Describe Conditions')
    riderHeight = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    riderHeight = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    riderWeight = models.DecimalField(max_digits=3, decimal_places=0, default=0)
    updated_at = models.DateTimeField(auto_now=True)

    # add relation to snowboard
    snowboard = models.ForeignKey('Snowboard', on_delete=models.CASCADE)
    reviewer = models.ForeignKey('Profile', on_delete=models.CASCADE)
    
    def __str__(self):
        return self.snowboard.name + " Review"

    def get_absolute_url(self):
        return reverse('person-detail', args=[str(self.id)])
class Terrain(models.Model):
    TERRAIN_CHOICES = (
        ('Freestyle', 'Freestyle'),
        ('All-Mountain', 'All-Mountain'),
        ('Freeride', 'Freeride'),
        ('Powder', 'Powder'),
    )
    name = models.CharField(max_length=50, choices=TERRAIN_CHOICES)

    def __str__(self):
        return self.name

# Size of snowboards
class Size(models.Model):
    # 4 for wide snowboard too, ex. 155W or 155MW
    size = models.CharField(max_length=15, null=True, blank=True)
# Snowboard objects
class Snowboard(models.Model):
    SKILL = (
        ('Beginner', 'Beginner'),
        ('Intermediate', 'Intermediate'),
        ('Expert', 'Expert'),
    )

    SHAPES = (
        ('Directional', 'Directional'),
        ('Directional Twin', 'Directional Twin'),
        ('Tapered Directional', 'Tapered Directional'),
        ('True Twin', 'True Twin'),
        ('Twin', 'Twin'),
    )

    PROFILES = (
        ('Flat', 'Flat'),
        ('Camber', 'Camber'),
        ('Rocker', 'Rocker'),
        ('Hybrid Camber', 'Hybrid Camber'),
        ('Hybrid Rocker', 'Hybrid Rocker'),    
    )

    season = models.CharField(max_length=20, default='Unknown')
    terrain = models.ManyToManyField(Terrain)
    shape = models.CharField(max_length=20, choices=SHAPES, default=SHAPES[0][0])
    profile = models.CharField(max_length=20, choices=PROFILES, default=PROFILES[0][0])
    rider = models.CharField(max_length=20, choices=SKILL, default=SKILL[0][0])
    sizes = models.ManyToManyField(Size)
    flex = models.IntegerField(default=0)
    brand = models.CharField(max_length=20, default='Unknown')
    name = models.CharField(max_length=50, default='Unknown')
    desc = models.CharField(max_length=500, default='No description available')
    image = models.ImageField(upload_to='snowboards/', null=True, default='snowboards/blank.jpg')
    brand_image = models.ImageField(upload_to='brands/', null=True, blank=True)


    def delete(self, *args, **kwargs):
        logger = logging.getLogger(__name__)
        # Delete the image and brand image files if they exist
        try:
            if self.image:
                self.image.delete(save=False)
            if self.brand_image:
                self.brand_image.delete(save=False)
        except Exception as e:
            logger.error(f"Error deleting image files for {self}: {e}")
            
        super().delete(*args, **kwargs)

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('snowboard-detail', args=[str(self.id)])

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_reviewer = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

    def get_absolute_url(self):
        return reverse('profile-detail', args=[str(self.id)])

class Comment(models.Model):
    # one to many relationships with snowboard and profile
    # comment section will be deleted if snowboard or profile is deleted
    snowboard = models.ForeignKey(Snowboard, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    comment_text = models.TextField(default="Add text here", validators=[MaxLengthValidator(200)])
    updated_at = models.DateTimeField(auto_now=True)
    
    
    def upvotes(self):
        return self.vote_set.filter(value=True).count()
    
    def downvotes(self):
        return self.vote_set.filter(value=False).count()

    def has_upvoted(self, user):
        if user.is_authenticated:
            return Vote.objects.filter(profile=user.profile, comment=self).exists()
        else:
            return False

    def has_downvoted(self, user):
        return self.vote_set.filter(profile=user.profile, value=False).exists()

    def __str__(self):
        return f"{self.user.username}'s comment on {self.snowboard.name}"

    def get_absolute_url(self):
        return reverse('snowboard-detail', args=[str(self.snowboard.id)])

class Vote(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, null=True, blank=True)
    review = models.ForeignKey(Review, on_delete=models.CASCADE, null=True, blank=True)
    value = models.BooleanField(null=True)  # True for thumbs up, False for thumbs down, NULL allowed

    def get_absolute_url(self):
        if self.comment:
            return reverse('snowboard-detail', args=[str(self.comment.id)])
        elif self.review:
            return reverse('snowboard-detail', args=[str(self.review.id)])
        else:
            return reverse('home_view')