from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from listings.models import Listing, Booking, Review
from decimal import Decimal
from datetime import date, timedelta
import random

class Command(BaseCommand):
    help = 'Seed the database with sample listing data'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting database seeding...'))

        # Create sample users
        users_data = [
            {'username': 'host1', 'email': 'host1@example.com', 'first_name': 'John', 'last_name': 'Doe'},
            {'username': 'host2', 'email': 'host2@example.com', 'first_name': 'Jane', 'last_name': 'Smith'},
            {'username': 'guest1', 'email': 'guest1@example.com', 'first_name': 'Alice', 'last_name': 'Johnson'},
            {'username': 'guest2', 'email': 'guest2@example.com', 'first_name': 'Bob', 'last_name': 'Wilson'},
        ]

        created_users = []
        for user_data in users_data:
            user, created = User.objects.get_or_create(
                username=user_data['username'],
                defaults=user_data
            )
            created_users.append(user)
            if created:
                self.stdout.write(f'Created user: {user.username}')
            else:
                self.stdout.write(f'User already exists: {user.username}')

        # Create sample listings
        listings_data = [
            {
                'name': 'Cozy Downtown Apartment',
                'description': 'A beautiful apartment in the heart of the city with modern amenities.',
                'location': 'New York, NY',
                'pricepernight': Decimal('120.00'),
                'host_id': created_users[0]
            },
            {
                'name': 'Beach House Paradise',
                'description': 'Stunning beachfront property with ocean views and private beach access.',
                'location': 'Miami, FL',
                'pricepernight': Decimal('250.00'),
                'host_id': created_users[0]
            },
            {
                'name': 'Mountain Cabin Retreat',
                'description': 'Peaceful cabin in the mountains, perfect for a weekend getaway.',
                'location': 'Aspen, CO',
                'pricepernight': Decimal('180.00'),
                'host_id': created_users[1]
            },
            {
                'name': 'Urban Loft Studio',
                'description': 'Modern loft studio in trendy neighborhood with great restaurants nearby.',
                'location': 'San Francisco, CA',
                'pricepernight': Decimal('200.00'),
                'host_id': created_users[1]
            },
            {
                'name': 'Historic Townhouse',
                'description': 'Charming historic townhouse with period features and modern comforts.',
                'location': 'Boston, MA',
                'pricepernight': Decimal('160.00'),
                'host_id': created_users[0]
            },
        ]

        created_listings = []
        for listing_data in listings_data:
            listing, created = Listing.objects.get_or_create(
                name=listing_data['name'],
                defaults=listing_data
            )
            created_listings.append(listing)
            if created:
                self.stdout.write(f'Created listing: {listing.name}')
            else:
                self.stdout.write(f'Listing already exists: {listing.name}')

        # Create sample bookings
        booking_guests = [created_users[2], created_users[3]]
        for i, listing in enumerate(created_listings[:3]):
            start_date = date.today() + timedelta(days=random.randint(10, 30))
            end_date = start_date + timedelta(days=random.randint(2, 7))
            nights = (end_date - start_date).days
            total_price = listing.pricepernight * nights
            
            booking_data = {
                'property_id': listing,
                'user_id': random.choice(booking_guests),
                'start_date': start_date,
                'end_date': end_date,
                'total_price': total_price,
                'status': random.choice(['pending', 'confirmed'])
            }
            
            booking, created = Booking.objects.get_or_create(
                property_id=listing,
                user_id=booking_data['user_id'],
                start_date=start_date,
                defaults=booking_data
            )
            if created:
                self.stdout.write(f'Created booking: {booking.booking_id}')

        # Create sample reviews
        review_data = [
            {'rating': 5, 'comment': 'Amazing place! Highly recommended.'},
            {'rating': 4, 'comment': 'Great location and clean apartment.'},
            {'rating': 5, 'comment': 'Perfect for our vacation. Will book again!'},
            {'rating': 3, 'comment': 'Good value for money, but could use some updates.'},
        ]

        for i, listing in enumerate(created_listings[:4]):
            review_info = review_data[i]
            review, created = Review.objects.get_or_create(
                property_id=listing,
                user_id=random.choice(booking_guests),
                defaults={
                    'rating': review_info['rating'],
                    'comment': review_info['comment']
                }
            )
            if created:
                self.stdout.write(f'Created review: {review.review_id}')

        self.stdout.write(
            self.style.SUCCESS(
                f'Database seeding completed successfully!\n'
                f'Created {len(created_users)} users\n'
                f'Created {len(created_listings)} listings\n'
                f'Created {Booking.objects.count()} bookings\n'
                f'Created {Review.objects.count()} reviews'
            )
        )