from django import forms
from .models import *



class LoginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)


class RegisterForm(forms.Form):
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)
    
    
class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['content', 'image', 'video']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['name', 'bio', 'instagram_url', 'profile_image']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(UserProfileForm, self).__init__(*args, **kwargs)
        if self.user:
            self.fields['name'].initial = self.user.username

    def save(self, commit=True):
        instance = super(UserProfileForm, self).save(commit=False)
        instance.user = self.user
        if commit:
            instance.save()
        return instance
