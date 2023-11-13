from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path('login/', views.user_login, name='login'),
    path('signup/', views.user_signup, name='signup'),
    path('logout/', views.user_logout, name='logout'),
    path("products/<slug:slug>", views.products_by_category, name="products"),
    path("cart/", views.cart, name="cart"),
    path("checkout/", views.checkout, name="checkout"),
    path("update_cart/", views.update_cart, name="update_cart"),
    path("get_cart_quantity/", views.get_cart_quantity, name="get_cart_quantity"),
]
