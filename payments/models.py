from django.db import models
from django.core.validators import RegexValidator
from users.models import User


class Payment(models.Model):
    full_name = models.CharField(max_length=255)
    card_type_choices = [
        ('VISA', 'Visa'),
        ('MC', 'MasterCard'),
        ('AMEX', 'American Express'),
    ]
    card_type = models.CharField(max_length=5, choices=card_type_choices)
    card_number = models.CharField(max_length=20)
    expiration = models.CharField(
        max_length=5, validators=[RegexValidator(r'^(0[1-9]|1[0-2])\/([0-9]{2})$', 'Enter a valid expiration date (MM/YY)')]
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateTimeField(auto_now_add=True)
    status_choices = [
        ('PENDING', 'Pending'),
        ('COMPLETED', 'Completed'),
        ('FAILED', 'Failed'),
    ]
    
    status = models.CharField(max_length=10, choices=status_choices, default='PENDING')
    order_no=models.CharField(max_length=100)
    user=models.ForeignKey(User,null=True, on_delete=models.SET_NULL)
