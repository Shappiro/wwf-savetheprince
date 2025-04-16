from django.urls import path
from .views import spell_check, filebrowser, css, spell_check_callback

urlpatterns = [
    path('spellchecker/', spell_check, name='tinymce-spellchecker'),
    path('filebrowser/', filebrowser, name='tinymce-filebrowser'),
    path('tinymce4.css', css, name='tinymce-css'),
    path('spellcheck-callback.js', spell_check_callback, name='tinymce-spellcheck-callback')
]
