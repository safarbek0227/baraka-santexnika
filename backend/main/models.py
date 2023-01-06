from django.db import models
from account.models import User
from datetime import timedelta
from django.utils import timezone


class MontylyReport(models.Model):
    income = models.IntegerField('kirim')
    outcome = models.PositiveIntegerField('chiqim')
    sells = models.PositiveIntegerField('sotildi')
    stock = models.PositiveIntegerField('sotib olindi')
    created_at = models.DateTimeField("Created at", auto_now_add=True, blank=False)
    
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
		( 'Metr', 'metr'),
		('kg', 'kg'),
		('sonida', 'number'),
	)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name="group")
    name = models.CharField(max_length=256)
    measure = models.CharField(choices=MEASURE, max_length=256)
    quantity = models.PositiveIntegerField()
    buy = models.PositiveIntegerField()
    sell = models.PositiveIntegerField()
    is_calc = models.BooleanField(default=True)
    created_at = models.DateTimeField("Created at", auto_now_add=True)

    def save(self,*args, **kwargs):
        if self.is_calc:
            report = MontylyReport.objects.last()
            report.outcome = report.outcome + (self.quantity * self.buy)
            report.save()
            self.is_calc = False
        super(Product, self).save(*args, **kwargs)

    def __str__(self):        
        return f"{self.name}"
    
    class Meta:
        ordering = ['-id']
      

class HistoryProduct(models.Model):
    MODE = (
        ('add', 'qo\'shish' ),
        ('sale', 'Sotish')
    )
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='products', related_query_name="product")
    mode = models.CharField(choices=MODE, max_length=128)
    quantity = models.PositiveIntegerField()
    price = models.IntegerField(blank=True)
    is_calc = models.BooleanField(default=True)
    comment = models.TextField(blank=False)
    created_at = models.DateTimeField("Created at", auto_now_add=True)

    def save(self,*args, **kwargs):
        self.price = (self.quantity * self.product.sell)
        if self.is_calc:
            if self.mode == 'add':
                report = MontylyReport.objects.last()
                report.outcome = report.outcome + (self.quantity * self.product.buy)
                report.save()
                obj = Product.objects.get(id = self.product.id)
                obj.quantity = self.product.quantity + self.quantity
                obj.save()
            if self.mode == 'sale':
                report = MontylyReport.objects.last()
                report.income = report.income + (self.quantity * self.product.sell)
                report.save()
                obj = Product.objects.get(id = self.product.id)
                obj.quantity = self.product.quantity - self.quantity
                print(obj.quantity)
                obj.save()
            self.is_calc = False
        super(HistoryProduct, self).save(*args, **kwargs)
    

    def __str__(self):
        return f"{self.product.name}, {self.quantity}{self.product.measure}"   

    class Meta:
        ordering = ['-id']



class Cart(models.Model):
    history = models.ManyToManyField(HistoryProduct)
    total = models.PositiveIntegerField()
    comment = models.TextField()
    created_at = models.DateTimeField("Created at", auto_now_add=True)
    
    