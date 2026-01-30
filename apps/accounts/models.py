""" ============= IMPORTS ============== """
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from apps.utilities.models import CoreModel
from phonenumber_field.modelfields import PhoneNumberField

""" ============= USER PROFILE  MODEL =============== """
class Userprofile(CoreModel):
    """ Extented user porfile with user type and additional fields"""

    ''' --------- USER TYPES -------- '''
    class UserType(models.TextChoices):
        CUSTOMER = 'customer', 'Customer / End User'
        EDITOR  = 'editor', 'Editor'
        CHIEF_EDITOR = 'chielf_editor', 'Chief Editor'

    ''' --------- FIELDS ----------'''   
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    user_type = models.CharField(
        max_length=20,
        choices=UserType.choices,
        default=UserType.CUSTOMER
    )
    bio = models.TextField(blank=True, help_text="brief description about the user")
    avatar = models.ImageField(upload_to='%y/%m/%d',null=True, blank=True)

    phone = PhoneNumberField(region="PK") # type: ignore
    wetsite = models.URLField(blank=True)

    '''------- Editor Specific Fields --------'''
    is_varified = models.BooleanField(default=False, help_text="Editor verification status")
    specialization = models.CharField(max_length=100,blank=True,help_text="Editor's area of expetise")

    '''' ----- META INFO ----- '''
    class META:
        verbose_name = 'User Profile'
        verbose_name = 'User Profiles'

    ''' ----- STRING REPRESENTAION ------ '''    
    def __str__(self): # type: ignore
        return f"{self.user.username} - {self.get_user_type_display()}" # type: ignore
    
    ''' ----- CUSTOM PROPERTIES ----- '''
    @property
    def is_editor(self):
        return self.user_type in [self.UserType.EDITOR, self.UserType.CHIEF_EDITOR]
    
    @property
    def is_chief_editor(self):
        return self.user_type == self.UserType.CHIEF_EDITOR
    
    @property
    def can_publish(self):
        return self.user_type == self.UserType.CHIEF_EDITOR
    
    @property
    def can_review(self):
        return self.user_type == self.UserType.CHIEF_EDITOR
    

    """========= SIGNALS TO AUTO CREATE/UPDATE PROFILE =========== """

    @receiver(post_save, sender=User)
    def create_or_update_user_profile(sender, instance, created, **kwargs):
        ''' create or update automatically when User is saved '''
        if created:
            Userprofile.objects.create(user=instance)
        else:
            if hasattr(instance, 'prfile'):
                instance.profile.save()    

    