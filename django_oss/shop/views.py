from django.shortcuts import render, redirect
from django.http import HttpResponse,Http404,JsonResponse
import json
from django.core.serializers import serialize
from django.contrib.auth import authenticate, login, logout 

from shop.models import *
from shop.forms import *

# Homepage / all products
def index(request):
    #Query categories for nav
    categories = Category.objects.all()
    print(categories)
    #Query all products
    products = Product.objects.all()
    context = {'categories':categories, 'products':products}
    return render(request, 'shop/products.html', context)


# signup page
## based on => SOURCE: https://medium.com/@devsumitg/django-auth-user-signup-and-login-7b424dae7fab ##
def user_signup(request):
    categories = Category.objects.all()
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            user = User.objects.get(username=form.cleaned_data['username'])
            cust = Customer(user=user)
            cust.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'shop/signup.html', {'form': form, 'categories':categories},)


# login page
## SOURCE: https://medium.com/@devsumitg/django-auth-user-signup-and-login-7b424dae7fab ##
def user_login(request):
    categories = Category.objects.all()
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)    
                return redirect('index')
    else:
        form = LoginForm()
    return render(request, 'shop/login.html', {'form': form, 'categories':categories},)


# logout page
## SOURCE: https://medium.com/@devsumitg/django-auth-user-signup-and-login-7b424dae7fab ##
def user_logout(request):
    logout(request)
    return redirect('login')


# Web page that shows all products belonging to a specific web page
def products_by_category(request, slug):
    try:
        # Query categories for nav
        categories = Category.objects.all()
        # check if category is valid
        Category.objects.get(name=str(slug))
        # Query categories based on category
        products = Product.objects.filter(category__name=str(slug))
        context = {'categories':categories,'products':products}
    except Category.DoesNotExist:
        raise Http404("Category does not exist")
    return render(request, 'shop/products.html', context)


# Web page that shows the contents of the cart
def cart(request):
    # Query categories for nav
    categories = Category.objects.all()
    # logged in user
    if request.user.is_authenticated:
        customer = request.user.customer
        # Query all orderer products from user or create order if no open order is present
        order, create = Order.objects.get_or_create(customer=customer, complete=False)
        orderedproducts = order.orderedproduct_set.all()
    else:
        # anonymous shopping, disabled
        orderedproducts = []
        order = []
    context = {'categories':categories, 'orderedproducts': orderedproducts, 'order':order}
    return render(request, 'shop/cart.html', context)


# Checkout web page, for now orders are just being closed, since payment is out of scope
def checkout(request):
    # Query categories for nav
    categories = Category.objects.all()
    context = {'categories':categories}
    complete_order(request)
    return render(request, 'shop/checkout.html', context)


# Method that updates the items in the cart
def update_cart(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    customer =  request.user.customer
    product = Product.objects.get(id=productId)
    
    # Query all orderer products from user or create order if no open order is present
    order, create = Order.objects.get_or_create(customer=customer, complete=False)

    # Query the customers order if product is already orderer or not
    ordered_product, create = OrderedProduct.objects.get_or_create(order=order, product=product)
    
    if action == 'add':
        ordered_product.quantity+=1
    elif action== 'decrease':
        ordered_product.quantity-=1
    
    ordered_product.save()

    # if items go below 0 they should be deleted out of the cart
    if ordered_product.quantity <= 0:
        ordered_product.delete()
    
    return JsonResponse('product updated in cart', safe=False)


# Method to show the amount of items currently in cart
def get_cart_quantity(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        
        # Query all orderer products from user or create order if no open order is present
        order, create = Order.objects.get_or_create(customer=customer, complete=False)
        data ={'cart-quantity':order.total_products_in_order}
    else:
        # if there is no user, quantity must always be 0 because of no anonymous shopping
        data = {'cart-quantity':0}
    return JsonResponse(data)


# Function to finish orders since actually "ordering is out of scope"
def complete_order(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, create = Order.objects.get_or_create(customer=customer, complete=False)
        order.complete=True
        order.save()

