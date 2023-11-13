from django.db import models
from django.contrib.auth.models import User

#helper function so images get safed as the name property of an object
def rename_image(instance, filename):
    return instance.name + '.jpg'

# Customer Model
class Customer(models.Model):
  # use the default django user model to build customer on
  user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
  name = models.CharField(max_length=30, null=True)
  email = models.CharField(max_length=50, null=True)

  def __str__(self):
    return self.name
  

# Category Model
class Category(models.Model):
  name = models.CharField(max_length=30, null=False)
  
  def __str__(self):
    return self.name


# Product Model
class Product(models.Model):
  name = models.CharField(max_length=30, null=False)
  description = models.CharField(max_length=250, null=False)
  price = models.DecimalField(max_digits=5,decimal_places=2, null=False)
  inventory = models.IntegerField(null=False)
  # Many-to-one relationship. Many products fall into one category
  category = models.ForeignKey(Category, on_delete=models.CASCADE)
  image = models.ImageField(upload_to=rename_image)

  def __str__(self):
    return self.name


# Order Model
class Order(models.Model):
  # On delete is set.null, so when a customer wants to be forgotten according to art17 GDPR, the Order data does not get lost
  customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True)
  order_date = models.DateTimeField(auto_now_add=True)
  # Null must be true to save unfinished orders so customers can return
  complete = models.BooleanField(default=False, null=True, blank=False)
  transaction_id = models.CharField(max_length=250, null=True)

  @property
  def get_total_price(self):
    orderedproducts = self.orderedproduct_set.all()
    return sum([orderedproduct.get_total for orderedproduct in orderedproducts])

  @property
  def total_products_in_order(self):
    orderedproducts = self.orderedproduct_set.all()
    return sum([orderedproduct.quantity for orderedproduct in orderedproducts])

  def __str__(self):
    return str(self.id)


# Ordered product model
class OrderedProduct(models.Model):
  # An ordered product must always inherit and reference an existing product
  product = models.ForeignKey(Product, on_delete=models.SET_NULL, blank=True, null=True)
  # An ordered product always belongs to one order
  order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
  quantity = models.IntegerField(default=0, blank=True, null=True)
  added_date = models.DateTimeField(auto_now_add=True)

  @property
  def get_total(self):
    return self.product.price * self.quantity
  
  def __str__(self):
    return str(self.product.name) + " " + str(self.quantity) + 'x'


# Shipping model, out of scope for this assignment
"""
class Shipping(models.Model):
  # all fields are nullable, so when a customer wants to be forgotten according to art17 GDPR, the Order data does not get lost
  customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True)
  order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
  address = models.CharField(max_length=50, null=True)
  city = models.CharField(max_length=50, null=True)
  zipcode = models.CharField(max_length=50, null=True)
  processed_date = models.CharField(max_length=50, null=True)
"""