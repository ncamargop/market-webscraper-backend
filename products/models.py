from django.db import models

# Create your models here.

class Product(models.Model):
    id = models.AutoField(primary_key=True)
    product_name = models.CharField(max_length=255, db_column='productName')
    price = models.IntegerField()
    quantity = models.CharField(max_length=255)
    store = models.CharField(max_length=255)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    image = models.CharField(max_length=255)

    class Meta:
        db_table = 'products'  # To asign to django to use my table products in mysql


class Index(models.Model):
    date = models.DateField(primary_key=True)
    unweighted_index = models.FloatField()

    class Meta:
        db_table = 'index_prices'  
