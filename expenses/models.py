from django.db import models
from django.contrib.auth.models import User
from django.db.models import Q
import datetime
from django.dispatch import receiver
from django.db.models.signals import post_save

class ExpenseManager(models.Manager):
    def search(self, query=None):
        if query is None or query == "" or len(query) < 1:
            return self.get_queryset(), True

        results = self.get_queryset().filter(
            Q(amount__startswith = query) |
            Q(date__startswith = query) |
            Q(description__icontains = query) |
            Q(category__icontains = query) 
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


class Expenses(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(decimal_places=2, max_digits=10)
    date = models.DateField()
    description = models.TextField(null=True, blank=True)
    category = models.CharField(max_length = 150)

    objects = ExpenseManager()
    class Meta:
        verbose_name_plural = "Expenses"
        ordering = ['-date']

    def __str__(self):
        return self.owner.username

class Category(models.Model):
    name = models.CharField(max_length = 50)

    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ['-id']
    def __str__(self):
        return self.name


@receiver(post_save, sender = Expenses)
def add_category(sender, instance, created, **kwargs):
    category_name = instance.category
    if not Category.objects.filter(name__iexact = category_name).exists():
        Category.objects.create(name = category_name)

# post_save.connect(add_category, sender = Expenses)