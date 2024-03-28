from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.views import generic

# Create your models here.

# Review objects
class Review(models.Model):
    BOARD_SIZES = [(str(i), f"{i} cm") for i in range(130, 170)]
    
    boardSize = models.CharField(max_length=200, choices=BOARD_SIZES, default=BOARD_SIZES[0][0])
    date = models.DateField(default='2024-01-01')
    conditions = models.CharField(max_length=200, default='Describe Conditions')
    snow24 = models.DecimalField(max_digits=2, decimal_places=1, default=0)
    snow7 = models.DecimalField(max_digits=3, decimal_places=1, default=0)
    riderHeight = models.DecimalField(max_digits=2, decimal_places=1, default=0)
    riderWeight = models.DecimalField(max_digits=3, decimal_places=0, default=0)
    
    # add relation to snowboard
    snowboard = models.ForeignKey('Snowboard', on_delete=models.CASCADE)
    reviewer = models.ForeignKey('Profile', on_delete=models.CASCADE)
    
    def __str__(self):
        return self.name

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
    flex = models.IntegerField(default=0)
    brand = models.CharField(max_length=20, default='Unknown')
    name = models.CharField(max_length=50, default='Unknown')
    desc = models.CharField(max_length=500, default='No description available')
    image = models.ImageField(upload_to='snowboards/', null=True)
    brand_image = models.ImageField(upload_to='brands/', null=True)
    # need to add image, rider, and brand image

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
    snowboard = models.ForeignKey(Snowboard, on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True)
    comment_text = models.TextField(default="Add text here")  # add a field to store the comment text

    def __str__(self):
        return f"{self.profile.user.username}'s comment on {self.snowboard.name}"

    def get_absolute_url(self):
        return reverse('comment-detail', args=[str(self.id)])

# shared attributes of users and reviewers

