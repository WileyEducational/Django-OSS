from django.test import TestCase
from shop.models import *

class TestCategory(TestCase):
  def set_up():
    Category.objects.create(name="fruits")

  def test_valid_category(self):
    self.set_up
    Category.objects.create(name="fruits")
    category = Category.objects.get(name="fruits")
    self.assertEqual(category.name, "fruits")
    print("Valid category object created...")

class TestProduct(TestCase):
  def test_valid_product(self):
    TestCategory.set_up()
    category = Category.objects.get(name="fruits")
    product = Product.objects.create(name="banana", description="this is a banana", price=0.99, inventory=5,category=category)
    self.assertEqual(product.name, "banana")
    self.assertEqual(product.description, "this is a banana")
    self.assertEqual(product.price, 0.99)
    self.assertEqual(product.inventory, 5)
    self.assertEqual(product.category, category)
    print("Valid product object created...")

class TestOrder(TestCase):
  def set_up_customer():
    Customer.objects.create(name="tester")

  def test_order_object(self):
    Customer.objects.create(name="tester")
    customer = Customer.objects.get(name="tester")
    order = Order.objects.create(customer=customer)
    self.assertEqual(order.customer.name, "tester")
    self.assertEqual(order.id, 1)
    print("Valid Order object created...")


class TestOrderedProduct(TestCase):
  def set_up_ordered_product():
    TestCategory.set_up()
    category = Category.objects.get(name="fruits")
    TestOrder.set_up_customer()
    customer = Customer.objects.get(name="tester")
    order = Order.objects.create(customer=customer)
    product = Product.objects.create(name="banana", description="this is a banana", price=0.99, inventory=5,category=category)
    ordered_product = OrderedProduct.objects.create(order=order, product=product, quantity=1)
    return ordered_product

  def test_ordering_product(self):
    ordered_product = TestOrderedProduct.set_up_ordered_product()
    self.assertEqual(ordered_product.product.name, "banana")
    self.assertEqual(ordered_product.order.customer.name, "tester")
    self.assertEqual(ordered_product.quantity, 1)
    print("Valid OrderedProduct object created...")

    
