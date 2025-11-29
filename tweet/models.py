from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models import Count

class Tweet(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField(max_length=240)
    photo = models.ImageField(upload_to='photo/', blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)
    likes = models.ManyToManyField(User, related_name='tweet_likes', blank=True)
    def __str__(self):
        return f'{self.user.username}-{self.text[:10]}'
    def total_likes(self):
        return self.likes.count()
    
    def user_has_liked(self, user):
        return self.likes.filter(id=user.id).exists()


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profession = models.CharField(max_length=100, blank=True)
    email = models.CharField(max_length=200)
    is_verified=models.BooleanField(default=False)
    bio = models.TextField(blank=True)
    profile_photo = models.ImageField(upload_to='profile_photos/', blank=True, null=True)
   
    followers = models.ManyToManyField(
        User, related_name='following', blank=True
    )
    def __str__(self):
        return self.user.username

    @property
    def following_count(self):
        return self.user.following.count()

    @property
    def followers_count(self):
        return self.followers.count()
    def total_likes_received(self):
        """Count total likes across all user's tweets - FIXED VERSION"""
        # Method 1: Using database aggregation (more efficient)
        return Tweet.objects.filter(user=self.user).aggregate(
            total_likes=Count('likes')
        )['total_likes'] or 0
    

from django.db import models
from django.contrib.auth.models import User
from django.db.models import Count
from .models import Tweet, UserProfile  # Safe import if models are in the same app

class Review(models.Model):
    SENTIMENT_CHOICES = [
        ('positive', 'Positive'),
        ('neutral', 'Neutral'),
        ('negative', 'Negative'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Who wrote the review
    tweet = models.ForeignKey(Tweet, on_delete=models.CASCADE, null=True, blank=True)  
    profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, null=True, blank=True)

    rating = models.IntegerField(default=0)     # 1–5 stars
    text = models.TextField()
    sentiment = models.CharField(max_length=10, choices=SENTIMENT_CHOICES, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review by {self.user.username} - {self.rating}★"