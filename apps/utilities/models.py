from django.db import models
import uuid

""" ======== Custom Manager for Core Model ========= """

class CoreManager(models.Model):
    def get_queryset(self):
        return super().get_queryset().filter(is_active=True)
    


""" ========= Base Model With Common Fields =========="""   

class CoreModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    objects = CoreManager()

    class Meta:
        abstract = True
        
    def __str__(self):
        return self.id

    def __repr__(self):
        return f"<{self.__class__.__name__} {self.id}>" 
    
    def activate(self):
        self.is_active = True
        self.save()

    def deactivate(self):
        self.is_active = False
        self.save()    

