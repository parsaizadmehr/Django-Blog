from django import forms
from .models import Comment

class ContactUsForm(forms.Form):
    name = forms.CharField(max_length=150)
    email = forms.EmailField()
    message = forms.CharField(widget=forms.Textarea)


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["name", "email", "body"]