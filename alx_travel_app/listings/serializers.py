from rest_framework import serializers
from .models import Listing, Booking, Review
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    """Serializer for User model"""
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email']

class ListingSerializer(serializers.ModelSerializer):
    """Serializer for Listing model"""
    host_id = UserSerializer(read_only=True)
    
    class Meta:
        model = Listing
        fields = [
            'listing_id', 'host_id', 'name', 'description', 
            'location', 'pricepernight', 'created_at', 'updated_at'
        ]
        read_only_fields = ['listing_id', 'created_at', 'updated_at']

class BookingSerializer(serializers.ModelSerializer):
    """Serializer for Booking model"""
    property_id = ListingSerializer(read_only=True)
    user_id = UserSerializer(read_only=True)
    
    class Meta:
        model = Booking
        fields = [
            'booking_id', 'property_id', 'user_id', 'start_date', 
            'end_date', 'total_price', 'status', 'created_at'
        ]
        read_only_fields = ['booking_id', 'created_at']

    def validate(self, data):
        """Validate booking dates"""
        if data['start_date'] >= data['end_date']:
            raise serializers.ValidationError("End date must be after start date.")
        return data

class ReviewSerializer(serializers.ModelSerializer):
    """Serializer for Review model"""
    property_id = ListingSerializer(read_only=True)
    user_id = UserSerializer(read_only=True)
    
    class Meta:
        model = Review
        fields = [
            'review_id', 'property_id', 'user_id', 'rating', 
            'comment', 'created_at'
        ]
        read_only_fields = ['review_id', 'created_at']