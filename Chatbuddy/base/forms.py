from dataclasses import field
from django.forms import ModelForm
from .models import Room
from django.contrib.auth.models import User


class roomForm(ModelForm):
    class Meta:
        model = Room
        fields = '__all__'
        exclude = ['host','participents']



class UserForm(ModelForm):
    class Meta:
        model = User
        fields =['username','email']