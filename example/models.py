from django.db import models


class Product(models.Model):
    collection = models.ForeignKey('ProductCollection', to_field='slug')


class ProductCollection(models.Model):
    slug = models.CharField(max_length=255, unique=True)
