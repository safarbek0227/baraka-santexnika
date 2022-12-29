from django.db import models
from account.models import User
from datetime import timedelta
from django.utils import timezone


# Create your models here.
def one_month_from_today():
    return timezone.now() + timedelta(days=30)


class MontylyReport(models.Model):
    income = models.IntegerField('kirim')
    outcome = models.PositiveIntegerField('chiqim')
    sells = models.PositiveIntegerField('sotildi')
    stock = models.PositiveIntegerField('sotib olindi')
    end_date  = models.DateField(default=one_month_from_today, blank=True, null=True)

    def __str__(self):
        return f"Kirim: {self.income}, Chiqim: {self.outcome}, Sotildi: {self.sells}, Sotil olindi{self.stock}"

    class Meta:
        ordering = ['-id']


class Todo(models.Model):
    name = models.CharField(max_length=256)
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name}"

class Group(models.Model):
    name = models.CharField('nomi', max_length=128)
    slug = models.SlugField('slug', max_length=128)

    def __str__(self):
        return f"{self.name}" 
    
    class Meta:
        ordering = ['-id']


class Product(models.Model):
    MEASURE = (
		( 'Metrida', 'metr'),
		('kg', 'kg'),
		('sonida', 'number'),
	)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name="group")
    name = models.CharField(max_length=256)
    measure = models.CharField(choices=MEASURE, max_length=256)
    quantity = models.PositiveIntegerField()
    buy = models.PositiveIntegerField()
    sell = models.PositiveIntegerField()
    comment = models.TextField(blank=True)
    is_calc = models.BooleanField(default=True)

    def save(self,*args, **kwargs):
        if self.is_calc:
            report = MontylyReport.objects.last()
            report.outcome = report.outcome + (self.quantity * self.buy)
            report.stock = report.stock + self.quantity
            report.save()
            self.is_calc = False
        super(Product, self).save(*args, **kwargs)

    def __str__(self):


        
        return f"{self.name}"
      

class HistoryProduct(models.Model):
    MODE = (
        ('add', 'qo\'shish' ),
        ('sale', 'Sotish')
    )
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='products', related_query_name="product")
    mode = models.CharField(choices=MODE, max_length=128)
    quantity = models.PositiveIntegerField()
    price = models.CharField(max_length=256, blank=True)
    is_calc = models.BooleanField(default=True)
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField("Created at", auto_now_add=True)

    def save(self,*args, **kwargs):
        self.price = f"{(self.quantity * self.product.sell)}"
        try:
            if self.is_calc:
                if self.mode == 'add':
                    report = MontylyReport.objects.last()
                    report.income = report.income + (self.quantity * self.product.sell)
                    report.sells = report.sells + self.quantity
                    report.stock = report.stock - self.quantity
                    report.save()
                    obj = Product.objects.get(id = self.product.id)
                    obj.quantity = self.product.quantity + self.quantity
                    obj.save()
                if self.mode == 'sale':
                    report = MontylyReport.objects.last()
                    report.outcome = report.outcome + (self.quantity * self.product.buy)
                    report.stock = report.stock - self.quantity
                    report.save()
                    obj = Product.objects.get(id = self.product.id)
                    obj.quantity = self.product.quantity - self.quantity
                    obj.save()
                self.is_calc = False
        except: pass
        super(HistoryProduct, self).save(*args, **kwargs)
    

    def __str__(self):
        return f"{self.product.name}, {self.quantity}{self.product.measure}"   

    class Meta:
        ordering = ['-id']



