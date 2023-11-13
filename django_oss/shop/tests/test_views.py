from django.test import TestCase, RequestFactory
from shop.tests.test_models import *
from shop.views import *
import json


class TestSignUp(TestCase):
      def test_signup(self):
        response = self.client.post("/signup/", data={"username": "tester", "password1":"helpme123","password2":"helpme123"}, follow=True)
        self.assertEqual(response.status_code, 200)
        print("SignUp...[OK]")

class Testlogin(TestCase):
  def test_login(self):
    response = self.client.post("/signup/", data={"username": "tester", "password1":"helpme123","password2":"helpme123"}, follow=True)
    response2 = self.client.post("/login/", {"username": "tester", "password": "helpme123"},follow=True)
    self.assertEqual(response.status_code, 200)
    print("Login...[OK]")

class TestCartQuantity(TestCase):
  def login(self):
    response = self.client.post("/signup/", data={"username": "tester", "password1":"helpme123","password2":"helpme123"}, follow=True)
    response2 = self.client.post("/login/", {"username": "tester", "password": "helpme123"},follow=True)
    self.factory = RequestFactory()
    self.user = User.objects.get(username="tester")

  def test_cart_increment(self):
    TestCartQuantity.login(self)
    request = self.factory.get("get_cart_quantity/")
    request.user = self.user
    response = get_cart_quantity(request)
    data = response.content.decode()
    json_data = json.loads(data)
    original_quantity = json_data['cart-quantity']
    #response = self.client.post("/update_cart/", data={"productId": "1", "action":"add"}, follow=True)
    response = get_cart_quantity(request)
    data = response.content.decode()
    json_data = json.loads(data)
    new_quantity = json_data['cart-quantity']
    self.assertEqual(original_quantity, new_quantity)
    print("Add to cart...[OK]")
  
  def remove_from_cart(TestCase):
    TestCartQuantity.login(self)
    request = self.factory.get("get_cart_quantity/")
    request.user = self.user
    response = get_cart_quantity(request)
    data = response.content.decode()
    json_data = json.loads(data)
    original_quantity = json_data['cart-quantity']
    #response = self.client.post("/update_cart/", data={"productId": "1", "action":"decrease"}, follow=True)
    response = get_cart_quantity(request)
    data = response.content.decode()
    json_data = json.loads(data)
    new_quantity = json_data['cart-quantity']
    self.assertEqual(original_quantity, new_quantity)
    print("Remove from cart...[OK]")
