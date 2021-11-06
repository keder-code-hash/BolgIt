 
from django import forms
from django.forms import ModelForm 
from posts.models import Posts
from django import forms
from .models import Comments
from mptt.forms import TreeNodeChoiceField


class NewCommentForm(forms.ModelForm):
    parent = TreeNodeChoiceField(queryset=Comments.objects.all())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['parent'].widget.attrs.update(
            {'class': 'd-none'})

        self.fields['parent'].label = ''
        self.fields['parent'].required = False

        self.fields['post'].widget.attrs.update(
            {'class': 'd-none'})

        self.fields['post'].label = ''
        self.fields['post'].required = False

    class Meta:
        model = Comments
        fields = ('parent', 'comment','post')

        widgets = {
            'content': forms.TextInput(attrs={'class': 'ml-3 mb-3 form-control border-0 comment-add rounded-0', 'rows': '1', 'placeholder': 'Add a public comment'}),
        }

    def save(self, *args, **kwargs):
        Comments.objects.rebuild()
        return super(NewCommentForm, self).save(*args, **kwargs)


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
