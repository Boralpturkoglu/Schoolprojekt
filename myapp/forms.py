from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django import forms
from .models import *

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email__iexact=email).exists():
            raise ValidationError("this e-mail already used.")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user

class GradeForm(forms.ModelForm):
    class Meta:
        model = Grade
        fields = ["value", "note"]  # Yalnızca öğretmenin eklemek istediği alanlar

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['title', 'anfang', 'ende', 'audience']
        widgets = {
            'anfang': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'ende': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['content','image','kategorie']
        widgets = {
            'content': forms.Textarea(attrs={'rows':3, 'placeholder':'Post your Idea...'}),
            'kategorie': forms.Select(attrs={'class': 'form-select'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["commentcontent"]
        widgets = {
            "commentcontent": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 3,
                "placeholder": "Write a comment..."
            })
        }

class QuizForm(forms.ModelForm):
    class Meta:
        model = Quiz
        fields = ['lesson', 'frage', 'antwort1', 'antwort2', 'antwort3', 'antwort4', 'richtigeantwort']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['lesson'].queryset = Lesson.objects.filter(teachers=user)

class UploadFileForm(forms.ModelForm):
    class Meta:
        model = File_Lernmaterial
        fields = ["lesson", "title", "file", "description"]  

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)
        if user:
         self.fields["lesson"].queryset = Lesson.objects.filter(teachers=user)


class KontaktForm(forms.Form):
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    subject = forms.CharField(max_length=200, required=False)
    text = forms.CharField(widget=forms.Textarea)

class PersonForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = ["phone", "profile_image", "branch"]

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ["address", "birth_date", "grade_level"]

class GeminiAiChatForm(forms.Form):
    question = forms.CharField(
        label="Ask Gemini",
        widget=forms.Textarea(attrs={"rows":3, "placeholder":"Type your question here..."}),
        max_length=500
    )