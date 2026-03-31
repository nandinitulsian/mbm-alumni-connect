from django.db import models
from accounts.models import User

class Opportunity(models.Model):
    TYPE_CHOICES = (
        ('internship', 'Internship'),
        ('job', 'Job'),
    )

    posted_by   = models.ForeignKey(User, on_delete=models.CASCADE, related_name='opportunities')
    company     = models.CharField(max_length=100)
    role        = models.CharField(max_length=100)
    type        = models.CharField(max_length=15, choices=TYPE_CHOICES)
    domain      = models.CharField(max_length=100, blank=True)
    stipend     = models.CharField(max_length=50, blank=True)
    deadline    = models.DateField(null=True, blank=True)
    apply_link  = models.URLField(blank=True)
    description = models.TextField()
    created_at  = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.company} - {self.role} ({self.type})"


class Application(models.Model):
    STATUS_CHOICES = (
        ('applied', 'Applied'),
        ('viewed', 'Viewed'),
        ('shortlisted', 'Shortlisted'),
        ('rejected', 'Rejected'),
    )

    student      = models.ForeignKey(User, on_delete=models.CASCADE, related_name='applications')
    opportunity  = models.ForeignKey(Opportunity, on_delete=models.CASCADE, related_name='applications')
    status       = models.CharField(max_length=15, choices=STATUS_CHOICES, default='applied')
    applied_at   = models.DateTimeField(auto_now_add=True)

    class Meta:
        # Student can only apply once to same opportunity
        unique_together = ('student', 'opportunity')
        ordering = ['-applied_at']

    def __str__(self):
        return f"{self.student.full_name} → {self.opportunity.company}"