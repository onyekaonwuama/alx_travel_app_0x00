from django.db import models
from django.contrib.auth.models import User
import uuid

class Listing(models.Model):
    """Model for property listings"""
    listing_id = models.UUIDField(
        primary_key=True, 
        default=uuid.uuid4, 
        editable=False
    )
    host_id = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='listings'
    )
    name = models.CharField(max_length=255)
    description = models.TextField()
    location = models.CharField(max_length=255)
    pricepernight = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-created_at']

class Booking(models.Model):
    """Model for booking reservations"""
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('canceled', 'Canceled'),
    ]
    
    booking_id = models.UUIDField(
        primary_key=True, 
        default=uuid.uuid4, 
        editable=False
    )
    property_id = models.ForeignKey(
        Listing, 
        on_delete=models.CASCADE, 
        related_name='bookings'
    )
    user_id = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='bookings'
    )
    start_date = models.DateField()
    end_date = models.DateField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Booking {self.booking_id} - {self.property_id.name}"

    class Meta:
        ordering = ['-created_at']

class Review(models.Model):
    """Model for property reviews"""
    review_id = models.UUIDField(
        primary_key=True, 
        default=uuid.uuid4, 
        editable=False
    )
    property_id = models.ForeignKey(
        Listing, 
        on_delete=models.CASCADE, 
        related_name='reviews'
    )
    user_id = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='reviews'
    )
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review {self.review_id} - {self.property_id.name}"

    class Meta:
        ordering = ['-created_at']
        unique_together = ['property_id', 'user_id']