from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    is_income = models.BooleanField(default=False)

    def __str__(self):
        return self.name
    

class Wallet(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    balance = models.PositiveIntegerField(default=0)
    
    def __str__(self):
        return self.name
    

class IncomeExpense(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE)
    summa = models.PositiveIntegerField()
    date_time = models.DateTimeField()
    is_income = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.summa} for {self.category.name}" 
