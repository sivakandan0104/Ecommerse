from django.db import models

class Member(models.Model):
    firstname = models.CharField(max_length=255)
    lastname = models.CharField(max_length=255)

class Register(models.Model):
    name = models.CharField(max_length=255)
    email = models.CharField(max_length=200)
    password = models.CharField(max_length=50)

class Mysqltable(models.Model):
    name = models.CharField(max_length=30)
    email = models.CharField(max_length=30, primary_key=True)
    password = models.CharField(max_length=200)

    class Meta:
        db_table = 'register'
        managed = False

class Products(models.Model):
    id = models.IntegerField( primary_key=True)
    name = models.CharField(max_length=30)
    price = models.IntegerField()

    class Meta:
        db_table = 'products'
        managed = False

class Cart(models.Model):
    user_name = models.CharField(max_length=30)
    product_name = models.CharField(max_length=30)
    price = models.IntegerField()
    quantity = models.IntegerField()
    status = models.CharField(max_length=20)

    class Meta:
        db_table = 'cart'
        managed = False

class orders(models.Model):
    id = models.IntegerField()
    order_id = models.CharField(max_length=100, primary_key=True)
    products = models.TextField()
    amount = models.IntegerField()
    payment_id = models.CharField(max_length=50)
    receipt = models.CharField(max_length=50)
    date_time = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20)

    class Meta:
        db_table ='orders'
        managed = False

'''class orderss(models.Model):
    order_id = models.CharField(max_length=100, primary_key=True)
    amount = models.IntegerField()
    currency = models.CharField(max_length=3)
    receipt = models.CharField(max_length=50)
    date_time = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20)
    payment_id = models.CharField(max_length=50,default='None')
    class Meta:
        db_table = 'orderss'
        managed = False '''

