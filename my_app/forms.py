from .models import Member
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class SignUpForm(UserCreationForm):
  class Meta:
    model = User
    fields = ('username', 'email', 'password1', 'password2')

class AddMemberForm(forms.ModelForm):
  class Meta:
    model = Member
    fields = ['name', 'age', 'image']

  def clean_name(self):
    name = self.cleaned_data.get('name')
    if not name.strip():
      raise forms.ValidationError('名前を入力してください。')
    
    if len(name) > 10:
      raise forms.ValidationError('10文字以内で入力してください。')
    
    return name
  