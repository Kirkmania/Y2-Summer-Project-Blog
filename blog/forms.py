from django import forms
from .models import Post, Comment, CV, Category

#choices = [('programming', 'Programming'), ('technology', 'Technology'), ('gaming', 'Gaming')]
choices = Category.objects.all().values_list('name','name')

class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('title', 'category', 'text',)

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.Select(choices=choices, attrs={'class': 'form-control'}),
            'text':  forms.TextInput(attrs={'class': 'form-control'}),
        }

class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('author', 'text',)

class CVForm(forms.ModelForm):

    class Meta:
        model = CV
        fields = ('text',)