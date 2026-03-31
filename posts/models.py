from django.db import models
from accounts.models import User

class Post(models.Model):
    POST_TYPE_CHOICES = (
        ('general', 'General'),
        ('query', 'Query'),
        ('resource', 'Resource'),
    )
    CATEGORY_CHOICES = (
        ('general', 'General'),
        ('placements', 'Placements'),
        ('projects', 'Projects'),
        ('internship', 'Internship'),
        ('technical', 'Technical'),
    )
    VISIBILITY_CHOICES = (
        ('open', 'Open to All'),
        ('branch', 'Branch Specific'),
    )

    author      = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    post_type   = models.CharField(max_length=10, choices=POST_TYPE_CHOICES, default='general')
    title       = models.CharField(max_length=200, blank=True)
    content     = models.TextField()
    category    = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='general')
    visibility  = models.CharField(max_length=10, choices=VISIBILITY_CHOICES, default='open')
    target_branch = models.CharField(max_length=100, blank=True)
    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.author.full_name} - {self.post_type} - {self.title[:30]}"

    def total_likes(self):
        return self.likes.count()

    def total_comments(self):
        return self.comments.count()


class Comment(models.Model):
    post            = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author          = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    content         = models.TextField()
    is_alumni_reply = models.BooleanField(default=False)
    created_at      = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"{self.author.full_name} on {self.post.title[:20]}"

    def save(self, *args, **kwargs):
        # Automatically mark as alumni reply if author is alumni
        if self.author.role == 'alumni':
            self.is_alumni_reply = True
        super().save(*args, **kwargs)


class Like(models.Model):
    post       = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')
    user       = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # One user can only like a post once
        unique_together = ('post', 'user')

    def __str__(self):
        return f"{self.user.full_name} liked {self.post.title[:20]}"
