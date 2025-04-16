from django import forms
from tinymce.widgets import TinyMCE
from .models import Post
from django.conf import settings

class PostForm(forms.ModelForm):
    new = forms.CharField(widget=TinyMCE(attrs={'cols': 30, 'rows': 5}))

    class Meta:
        model = Post
        fields = ('title','new','association','site')

