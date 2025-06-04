from django.db import models

class User (models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)

    def __str__(self):
        return self.name


class Transaction (models.Model):
    TYPES = [
        ('DEPOSIT', 'Deposit'),
        ('WITHDRAW', 'Withdraw'),
        ('TRANSFER', 'Transfer'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='transactions')
    tx_type = models.CharField(max_length=10, choices=TYPES)
    amount = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    description = models.TextField(blank=True)
    timestamp = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'{tx_type} - {amount}'

