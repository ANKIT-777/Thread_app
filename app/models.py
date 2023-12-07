# models.py
from django.db import models
from django.contrib.auth.models import User,AbstractUser

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey('Post', on_delete=models.CASCADE, related_name='post_comments')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE) 
    content = models.TextField()
    image = models.ImageField(upload_to='post_images/', blank=True, null=True)
    video = models.FileField(upload_to='post_videos/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    likes_count = models.PositiveIntegerField(default=0)
    liked_by = models.ManyToManyField(User, related_name='liked_posts', blank=True)
    comments = models.ManyToManyField(Comment, related_name='comment_posts', blank=True)

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, blank=True)
    bio = models.TextField(blank=True)
    instagram_url = models.URLField(blank=True)
    profile_image = models.ImageField(upload_to='profile_images/', blank=True, null=True)
    followers = models.ManyToManyField(User, related_name='following', blank=True)
    following = models.ManyToManyField(User, related_name='followers', symmetrical=False, blank=True)



        
