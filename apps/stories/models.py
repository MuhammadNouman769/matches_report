""" =========== IMPORTS ============ """
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse
from django.utils.text import slugify
from apps.utilities.models import CoreModel
from ckeditor_uploader.fields import RichTextUploadingField



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
    content = RichTextUploadingField(max_length=1000)
    image = models.ImageField(upload_to='stories/%Y/%m/%d', blank=True, null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='stories')
    status = models.CharField(max_length=10, choices=StoryStatus.choices,default=StoryStatus.Draft)
    tags = models.ForeignKey("StoryTag", on_delete=models.CASCADE, related_name='story_tags') # type:ignore
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
    review_notes = models.TextField(blank=True, help_text="Review comments from chief editor")
    

    ''' '''

""" ============ Story Chapter =========== """
class StoryChapter(CoreModel):
    story = models.ForeignKey(Story, on_delete=models.CASCADE, related_name='chapters')
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    content =  RichTextUploadingField(max_length=1000)
    image = models.ImageField(upload_to='chapter/%y/%m/%d',blank=True,null=True)
    video = models.FileField(upload_to='chapter/%y/%m/%d',blank=True,null=True)
    order = models.PositiveBigIntegerField(default=0)
    
    
    
    
    
    
    
""" ============== Story Like ============== """    
class StoryLike(CoreModel):
    story = models.ForeignKey(Story, on_delete=models.CASCADE, related_name='story_like')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    

""" ================ Story View ================ """
class StoryView(CoreModel):
    story = models.ForeignKey(Story,on_delete=models.CASCADE, related_name='story_views')  
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True,blank=True)
    id_adress = models.GenericIPAddressField(null=True,blank=True)
    
    
      
""" ============== Story Tags ============= """  
class StoryTag(CoreModel):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True) 
    
    class Meta: # pyright: ignore[reportIncompatibleVariableOverride]
        ordering = ['name']
        verbose_name_plural = 'Story Tags'
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        
        super().save( *args, **kwargs) 
        
    def __str__(self): # type: ignore
        return self.name       
           