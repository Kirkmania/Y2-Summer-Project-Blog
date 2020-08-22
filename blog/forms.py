from django import forms
from .models import Post, Comment, Category
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column

#choices = [('programming', 'Programming'), ('technology', 'Technology'), ('gaming', 'Gaming')]

class PostForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('title', css_class='form-group col-md-8 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('category', css_class='form-group col-md-3 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('text', css_class='form-group col-md-15 mb-0'),
                css_class='form-row'
            ),
            Submit('save_as_draft', 'Save as draft', css_class="btn btn-secondary"),
            Submit('save_and_publish', 'Save and publish', css_class="btn btn-secondary")
        )

    class Meta:
        choices = Category.objects.all().values_list('name','name')
        model = Post
        fields = ('title', 'category', 'text',)
        widgets = {
             'title': forms.TextInput(attrs={'class': 'form-control'}),
             'category': forms.Select(choices=choices, attrs={'class': 'form-control'}),
         }

class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('author', 'text',)
        widgets = {
            'author': forms.TextInput(attrs={'class': 'form-control'}),
            'text': forms.Textarea(attrs={'class': 'form-control'}),
        }