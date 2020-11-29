from django import forms
from .models import *

class ImageForm(forms.ModelForm):
    image = forms.ImageField(widget=forms.FileInput(attrs={'id':'image'}))
    class Meta:
        model = Image
        fields = ['image']
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.fields['image'].label=''
        self.fields['image'].help_text='Drag and Drop or upload'
