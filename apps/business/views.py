from django.core.mail import send_mail
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.conf import settings
from django.contrib import messages

from apps.seo.views import SEOListView, SEODetailView

from .models import Product

import stripe
import json

stripe.api_key = settings.STRIPE_PRIVATE

STRIPE_PUBLIC_KEY = settings.STRIPE_PUBLIC



class ProductsListView(SEOListView):
    model = Product
    meta_description = 'Las mejores herramientas para ser un mejor inversor, todo, al mejor precio, gratis.'
    meta_title = 'Las herramientas inteligentes para invertir como un experto'
    context_object_name = 'products'


class ProductDetailView(SEODetailView):
    model = Product





# def CHECKOUT(request):
    
#     meta_title = 'Caja'
    

#     context={
#             "STRIPE_PUBLIC_KEY": STRIPE_PUBLIC_KEY,
#             "meta_title":meta_title
#         }

#     return render (request, 'checkout.html', context )


# def CHECKOUT_SUBSCRIPTION(request, id):
#     if request.method == 'POST':
#         product = PRODUCT.objects.get(id = id)
#         if product.name == 'Membresía semestral':
#             mode = 'subscription'
#             price_id = product.stripe_price_id
#         elif product.name == 'Membresía de por vida':
#             mode = 'payment'
#             price_id = product.stripe_price_id
#         elif product.name == 'Excel de inversiones dinámico':
#             mode = 'subscription'
#             price_id = product.stripe_price_id
#         else:
#             mode = 'payment'
#             price_id = product.stripe_price_id
       
#         current_order = ORDER.objects.create(customer_session_id= request.COOKIES['sessionid'])
#         purchase= PURCHASE.objects.create(product_related= product,final_price= product.price, order_related = current_order)
#         current_order.purchases_related.add(purchase)
#         current_order.save()

#         try:
#             checkout_session = stripe.checkout.Session.create(  
#                 line_items= [{
#                 'price': price_id,
#                 # For metered billing, do not pass quantity
#                 'quantity': 1
#                     }],
#                 payment_method_types=['card'],
#                 mode = mode,
#                 success_url= 'https://inversionesyfinanzas.xyz/pago-correcto?session_id={CHECKOUT_SESSION_ID}'+f'&order_id={current_order.order_identification}',
#                 cancel_url= 'https://inversionesyfinanzas.xyz/checkout/',

#             )
            
#         except Exception as e:
         
#             return str(e)
        
#         return redirect(checkout_session.url, code=303)


# def CHECKOUT_SESSION_STRIPE(request):
#     if request.method == 'POST':

#         all_products_in_cart = Cart(request)
#         products_list = []
#         for prods in all_products_in_cart:
#             prod_id = prods['product']
#             products_list.append(PRODUCT.objects.get(id = prod_id.id))

#         if ORDER.objects.filter(customer_session_id= request.COOKIES['sessionid']).exists() != True:
#             current_order = ORDER.objects.create(customer_session_id= request.COOKIES['sessionid'])
#         else:
#             current_order = ORDER.objects.get(customer_session_id= request.COOKIES['sessionid'])
#         line_items_list = []
#         for item in products_list:
#             purchase= PURCHASE.objects.create(product_related= item,final_price= item.price, order_related = current_order)
#             line_item = {}
#             line_item["price"] = item.stripe_price_id
#             line_item["quantity"] = 1
#             line_items_list.append(dict(line_item))      
            
#             current_order.purchases_related.add(purchase)
#             current_order.save()
        
        
#         try:
#             checkout_session = stripe.checkout.Session.create(  
#                 line_items= line_items_list,
#                 payment_method_types=['card'],
#                 mode='payment',
#                 success_url= 'https://inversionesyfinanzas.xyz/pago-correcto?session_id={CHECKOUT_SESSION_ID}'+f'&order_id={current_order.order_identification}',
#                 cancel_url= 'https://inversionesyfinanzas.xyz/checkout/',

#             )
            
#         except Exception as e:
         
#             return str(e)
        
#         return redirect(checkout_session.url, code=303)

# def PAYMENT_SUCCEEDED(request):
#     if request.method == 'GET':
#         session = stripe.checkout.Session.retrieve(request.GET['session_id'])
#         customer = stripe.Customer.retrieve(session.customer)
       
#         customer_email = customer['email']

#         current_customer = CUSTOMER.objects.filter(email = customer_email)
#         if current_customer.exists() == True:
#             current_customer = CUSTOMER.objects.get(email = customer_email)
#         else:
#             current_customer = CUSTOMER.objects.create(email = customer_email, stripe_customer_id = customer['id'])

#         if request.user.is_anonymous == False:
#             CUSTOMER.objects.filter(email = customer_email).update(user_related = request.user)
        
#         current_order = ORDER.objects.filter(order_identification= request.GET['order_id'])

#         try:
#             for purchase in ORDER.objects.get(order_identification= request.GET['order_id']).purchases_related:
#                 PURCHASE.objects.filter(id = purchase.id).update(customer = current_customer)
#         except:
#             PURCHASE.objects.filter(order_related = ORDER.objects.get(order_identification= request.GET['order_id'])).update(customer = current_customer)

#         current_order.update(customer = current_customer, finished= True)
#         LINK_CUSTOMER_TO_USER.delay(customer_email)
#         Cart(request).clear()
#         messages.success(request, 'Tu pago se ha efectuado correctamente. Únete al Campus del Inversor Inteligente para tener acceder a tu compra.')
#         return redirect('register')