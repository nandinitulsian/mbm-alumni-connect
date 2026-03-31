from django.db import models
from accounts.models import User

class Connection(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    )

    student    = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_connections')
    alumni     = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_connections')
    status     = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        # Student can only send one request to same alumni
        unique_together = ('student', 'alumni')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.student.full_name} → {self.alumni.full_name} ({self.status})"