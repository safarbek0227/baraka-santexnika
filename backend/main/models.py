from django.db import models
from account.models import User
from datetime import timedelta
from django.utils import timezone


# Create your models here.
def one_month_from_today():
    return timezone.now() + timedelta(days=30)


class MontylyReport(models.Model):
    factory = models.ForeignKey(User, on_delete=models.CASCADE, related_name="report", default=None, null=True)
    income = models.PositiveIntegerField('kirim')
    outcome = models.PositiveIntegerField('chiqim')
    sells = models.PositiveIntegerField('sotildi')
    buy = models.PositiveIntegerField('sotib olindi')
    end_date  = models.DateField(default=one_month_from_today, blank=True, null=True)

    def __str__(self):
        return f"Kirim: {self.income}, Chiqim: {self.outcome}, Sotildi: {self.sells}, Sotil olindi{self.buy}"

    class Meta:
        ordering = ['-id']


class Todo(models.Model):
    factory = models.ForeignKey(User, on_delete=models.CASCADE, related_name="Todo")
    name = models.CharField(max_length=256)
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name}"

class Group(models.Model):
    factory = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user")
    name = models.CharField('nomi', max_length=128)
    slug = models.SlugField('slug', max_length=128)

    def __str__(self):
        return f"{self.name}" 
    
    class Meta:
        ordering = ['-id']


class Product(models.Model):
    MEASURE = (
		('metr', 'Metrida'),
		('weight', 'o\'girligida'),
		('number', 'sonida'),
	)
    factory = models.ForeignKey(User, on_delete=models.CASCADE, related_name="product")
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name="group")
    name = models.CharField(max_length=256)
    measure = models.CharField(choices=MEASURE, max_length=256)
    quantity = models.PositiveIntegerField()
    buy = models.PositiveIntegerField()
    sell = models.PositiveIntegerField()
    comment = models.TextField(blank=True)

    def __str__(self):
        return f"{self.name}"

class HistoryProduct(models.Model):
    factory = models.ForeignKey(User, on_delete=models.CASCADE, related_name="history")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product')
    quantity = models.PositiveIntegerField()
    price = models.CharField(max_length=256, blank=True)
    is_calc = models.BooleanField(default=True)
    comment = models.TextField(blank=True)

    def save(self,*args, **kwargs):
        self.price = f"{(self.quantity * self.product.sell) / 1000} ming"
        try:
            if self.is_calc:
                obj = Product.objects.get(id = self.product.id)
                obj.quantity = self.product.quantity - self.quantity
                obj.save()
                self.is_calc = False
        except: pass
        report = MontylyReport.objects.get(factory_id = self.factory.id)
        report.income = report.outcome + (self.quantity * (self.product.sell - self.product.buy))
        report.sells = report.sells + self.quantity
        report.save()
        super(HistoryProduct, self).save(*args, **kwargs)
    

    def __str__(self):
        return f"{self.product.name}, {self.quantity}{self.product.measure}"   

    class Meta:
        ordering = ['-id']



