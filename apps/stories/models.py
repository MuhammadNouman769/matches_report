""" =========== IMPORTS ============ """
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse
from django.utils.text import slugify
from apps.utilities.models import CoreModel


""" ============= Story Model ============"""
class Story(models.Model):
    '''Model for story/news field'''

    class StoryStatus(models.TextChoices):
        Draft = 'draft', 'Draft'
        REVIEW = 'review', 'Under Review'
        PUBLISHED = 'published', 'Bublished'
        REJECTED = 'rejected', 'Rejected'
        CANCEL = 'cancel', 'Cancel'


    ''' ------- core fields -------- '''
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    content = models.TextField()
    image = models.ImageField(upload_to='stories/%Y/%m/%d', blank=True, null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='stories')
    status = models.CharField(max_length=10, choices=StoryStatus.choices,default=StoryStatus.Draft)
    tags = models.ForeignKey()
    
    '''Meta Data'''
    summery = models.TextField(blank=True, help_text="Brief summery of story")
    published_at = models.DateTimeField(null=True, blank=True)

    '''Review work flow'''
    reviewed_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,related_name='rewieved_stories'
    )
    reviewed_at = models.TextField(blank=True, help_text="Review comments from chief editor")

    ''' '''

