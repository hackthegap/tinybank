from django.db import models

class User(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)

    def __str__(self):
        return self.name

class Transaction(models.Model):
    TYPES = [
        ('DEPOSIT', 'Deposit'),
        ('WITHDRAW', 'Withdraw'),
        ('TRANSFER', 'Transfer'),
    ]

    user = models.ForeignKey('User', on_delete=models.CASCADE, related_name='transactions')
    tx_type = models.CharField(max_length=10, choices=TYPES)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    description = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        super().save(*args, **kwargs)
        if is_new:
            user = self.user
            if self.tx_type == 'DEPOSIT':
                user.balance += self.amount
            elif self.tx_type in ['WITHDRAW', 'TRANSFER']:
                user.balance -= self.amount
            user.save()

    def delete(self, *args, **kwargs):
        user = self.user
        # Revert balance based on type
        if self.tx_type == 'DEPOSIT':
            user.balance -= self.amount
        elif self.tx_type in ['WITHDRAW', 'TRANSFER']:
            user.balance += self.amount
        user.save()
        super().delete(*args, **kwargs)
