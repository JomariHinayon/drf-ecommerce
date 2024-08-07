from django.db import models
from mptt.models import MPTTModel, TreeForeignKey


class ActiveQuerySet(models.QuerySet):

    def isactive(self):
        return self.filter(is_active=True)

class Category(MPTTModel):
    name = models.CharField(max_length=255, unique=True)
    is_active = models.BooleanField(default=False)
    
    # parent
    parent = TreeForeignKey('self', on_delete=models.PROTECT, null=True, blank=True)

    # manager
    objects = ActiveQuerySet.as_manager()

    def __str__(self):
        return self.name
    
    class MPTTMeta:
        order_insertion_by = ['name']
    
class Brand(models.Model):
    name = models.CharField(max_length=255, unique=True)
    is_active = models.BooleanField(default=False)

    # manager
    objects = ActiveQuerySet.as_manager()

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255)
    description = models.TextField(max_length=1000)
    is_digital = models.BooleanField(default=False)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    category = TreeForeignKey('Category', on_delete=models.SET_NULL, null=True, blank=True)
    is_active = models.BooleanField(default=False)

    # manager
    objects = ActiveQuerySet.as_manager()

    def __str__(self):
        return self.name
    
class ProductLine(models.Model):
    price = models.DecimalField(max_digits=8, decimal_places=2)
    sku = models.CharField(max_length=255)
    stock_qty = models.IntegerField()
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="product_line")
    is_active = models.BooleanField(default=False)

    # manager
    objects = ActiveQuerySet.as_manager()

    def __str__(self):
        return self.product.name
