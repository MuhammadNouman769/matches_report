from django import forms
from .models import Story,StoryChapter
from django.core.exceptions import ValidationError
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django.forms import inlineformset_factory,BaseInlineFormSet

""" ========== Story Create Form =========== """

class StoryForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorUploadingWidget())

    class Meta:
        model = Story
        fields = ['title', 'content', 'image', 'tags', 'summery']

""" =========== Story Chapter Form ========== """
class StoryChapterForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorUploadingWidget)

    class Meta:
        model = StoryChapter
        fields = ['title', 'content', 'image', 'video', 'order']

"""==== Custom Formset for Validations ===="""
class ConditionalChapterFormSet(BaseInlineFormSet):
    def clean(self):
        super().clean()
        count = 0
        for form in self.forms:
            if not form.cleaned_data.get("DELETE", False) and form.cleaned_data:
                count+=1
        
        story = self.instance
        story_status = getattr(story, "status", None)

        if story_status in ["submitted", "published"] and count < 1:
            raise ValidationError("At least one chapter in required before sibmitting or publishing this story.")
            


""" inline formset for story-chapters """             
StoryChapterFormSet = inlineformset_factory(
    Story,
    StoryChapter,
    form=StoryChapterForm,
    formset=ConditionalChapterFormSet,
    extra=1,
    can_delete=True
)

