from django.db import models
import datetime
from django.contrib.auth.models import User
from django.utils import timezone


class Publisher(models.Model):
    name = models.CharField(max_length=200)
    website = models.URLField()
    city = models.CharField(max_length=20, blank=True)
    country = models.CharField(max_length=50, default='USA')

    def __str__(self):
        return self.name


class Book(models.Model):
    CATEGORY_CHOICES = [
        ('S', 'Science&Tech'),
        ('F', 'Fiction'),
        ('B', 'Biography'),
        ('T', 'Travel'),
        ('O', 'Other')
    ]
    title = models.CharField(max_length=200)
    category = models.CharField(max_length=1, choices=CATEGORY_CHOICES, default='S')
    num_pages = models.PositiveIntegerField(default=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    publisher = models.ForeignKey(Publisher, related_name='books', on_delete=models.CASCADE)
    description = models.TextField(blank=True, null=True)
    num_reviews = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title

class Review(models.Model):
    reviewer = models.EmailField()
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField()
    comments = models.TextField(blank=True)
    date = models.DateField(default=timezone.now)

    def __str__(self):
        return f"Review by {self.reviewer} for {self.book}"

class Member(User):
    MEMBER_STATUS_CHOICES = [
            (1, 'Regular member'),
            (2, 'Premium Member'),
            (3, 'Guest Member'),
        ]

    status = models.IntegerField(choices=MEMBER_STATUS_CHOICES, default=1)
    address = models.CharField(max_length=300)
    city = models.CharField(max_length=20, default='Windsor')
    province = models.CharField(max_length=2, default='ON')
    last_renewal = models.DateField(default=timezone.now)
    auto_renew = models.BooleanField(default=True)
    borrowed_books = models.ManyToManyField(Book, blank=True)


class Order(models.Model):
    ORDER_TYPE_CHOICES = [
        (1, 'Type 1'),
        (2, 'Type 2')
    ]
    STATUS_CHOICES = [
        ('Purchased', 'Purchased'),
        ('Confirmed', 'Confirmed'),
        ('Cancelled', 'Cancelled')
    ]
    order_type = models.IntegerField(choices=ORDER_TYPE_CHOICES)
    member = models.ForeignKey(Member, related_name='orders', on_delete=models.CASCADE)
    books = models.ManyToManyField(Book, related_name='orders')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Purchased')  # Add max_length attribute

    def __str__(self):
        return f'Order {self.id} - {self.get_order_type_display()}'

