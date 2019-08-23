from django import forms
from .models import Job,Category,Application


class PostForm(forms.ModelForm):

    class Meta:
        model = Job
        fields = ('title','category')
    


