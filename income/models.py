from django.db import models
from django.contrib.auth.models import User
from django.db.models import Q
import datetime
class IncomeManager(models.Manager):
    def search(self, query=None):
        if query is None or query == "" or len(query) < 1:
            return self.get_queryset(), True

        results = self.get_queryset().filter(
            Q(amount__startswith = query) |
            Q(date__startswith = query) |
            Q(description__icontains = query) |
            Q(source__icontains = query) 
        )
        return results, False
    def time_amount_filter(self, time):
        '''
            This returns a qs filtered by the time provided, as well as the total amount 
        '''
        amount = 0
        date_now = datetime.date.today()
        result = self.get_queryset().filter(
            date__gte = time, 
            date__lte = date_now
        )
        for item in result:
            amount += item.amount 

        return {
            'queryset' : result ,
            'amount' : amount
        }

class Income(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(decimal_places=2, max_digits=10)
    date = models.DateField()
    description = models.TextField(null=True, blank=True)
    source = models.CharField(max_length = 150)

    objects = IncomeManager()
    class Meta:
        verbose_name_plural = "Income"
        ordering = ['-date']

    def __str__(self):
        return self.owner.username

# class Category(models.Model):
#     name = models.CharField(max_length = 50)

#     class Meta:
#         verbose_name_plural = 'Categories'

#     def __str__(self):
#         return self.name