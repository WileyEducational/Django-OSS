from django.contrib import admin
from shop.models import *

admin.site.register(Customer)
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(OrderedProduct)

# Out of scope for this assignment
# admin.site.register(Shipping)
