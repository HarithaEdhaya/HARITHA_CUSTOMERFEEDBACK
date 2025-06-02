from django.db import models
from django.utils.timezone import now

class Feedback(models.Model):
    CATEGORY_CHOICES = [
        ('product', 'Product Satisfaction'),
        ('service', 'Service Quality'),
        ('experience', 'Overall Experience'),
    ]

    RATING_CHOICES = [(i, str(i)) for i in range(1, 6)]

    name = models.CharField(max_length=100)
    email = models.EmailField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    message = models.TextField()
    rating = models.IntegerField(choices=RATING_CHOICES)

    # 🔽 NEW FIELDS
    admin_response = models.TextField(blank=True, null=True)
    responded_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"{self.name} - {self.category} - {self.rating}/5"
