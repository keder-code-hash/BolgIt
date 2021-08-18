# from markdownx.fields import MarkdownxFormField
from django import forms
from django.forms import ModelForm
# from mdeditor.fields import MDTextFormField
from posts.models import Posts

# class markDownForm(forms.Form):
#     myField = MarkdownxFormField()

class postDetails(forms.Form):
    like=forms.BooleanField()
    save=forms.BooleanField()


class postsCreateForm(ModelForm):
    class Meta:
        model=Posts
        fields='__all__'
        exclude=['owner','post_like','status']
    def clean(self):
        cleaned_data=super().clean()
        return cleaned_data

            # 'post_title':('Title'),
            # 'post_catagory':('Catagory'),
