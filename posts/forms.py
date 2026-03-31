from django import forms

from .models import Comment, Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['post_type', 'title', 'content', 'category', 'visibility', 'target_branch']
        widgets = {
            'post_type': forms.Select(),
            'title': forms.TextInput(attrs={'placeholder': 'Add a short title'}),
            'content': forms.Textarea(
                attrs={
                    'placeholder': 'Share an update, ask a question, or post a useful resource...',
                    'rows': 6,
                }
            ),
            'category': forms.Select(),
            'visibility': forms.Select(),
            'target_branch': forms.TextInput(attrs={'placeholder': 'e.g. Computer Science'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        visibility = cleaned_data.get('visibility')
        target_branch = (cleaned_data.get('target_branch') or '').strip()

        if visibility == 'branch' and not target_branch:
            self.add_error('target_branch', 'Please choose the branch for this post.')

        if visibility == 'open':
            cleaned_data['target_branch'] = ''

        return cleaned_data


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(
                attrs={
                    'placeholder': 'Write your comment...',
                    'rows': 3,
                }
            ),
        }
