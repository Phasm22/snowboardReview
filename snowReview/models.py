from django.db import models
from django.urls import reverse
from django.views import generic

# Create your models here.

# Review objects
class Review(models.Model):
    pass

# Comment objects
class Comments(models.Model):
    pass

# Snowboard objects
class Snowboard(models.Model):
    pass

# shared attributes of users and reviewers
class Person(models.Model):
    # List of experience levels
    EXPERIENCE = (
        ('Beginner', 'Beginner'),
        ('Intermediate', 'Intermediate'),
        ('Expert', 'Expert'),
    )

    name = models.CharField(max_length=100, default='Anonymous')
    email = models.EmailField("Email", max_length=200)
    experience = models.CharField(max_length=100, choices=EXPERIENCE, default='Beginner')


    # General Users
    class User(models.Model):
        pass

    # Admins
    class Reviewer(models.Model):
        # relationship for reviewer to review
        review = models.ForeignKey(Review, on_delete=models.CASCADE)
        pass
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('person-detail', args=[str(self.id)])