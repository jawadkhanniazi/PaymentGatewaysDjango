from django.shortcuts import render
import os
from flask import Flask, redirect, request
from django.views import View
from django.views.generic import TemplateView
import stripe
from django.conf import settings
from django.http import JsonResponse, HttpResponse
from .models import Product,OrderDetails
from products.models import OrderDetails
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail


# Create your views here.

stripe.api_key = settings.STRIPE_SECRET_KEY

class SuccessView(TemplateView):
    template_name = "success.html"


class CancelView(TemplateView):
    template_name = "cancel.html"

class ProductLandingPAgeView(TemplateView):
    template_name = "landing.html"
    def get_context_data(self, **kwargs):
        product = Product.objects.get(name="Test Product")
        context =  super(ProductLandingPAgeView, self).get_context_data(**kwargs)
        context.update({'STRIPE_PUBLIC_KEY':settings.STRIPE_PUBLIC_KEY, 'product':product})
        return context

class CreateCheckoutSessionView(View):
    def post(self, request, *args, **kwargs):
        #price = Price.objects.get(id=self.kwargs["pk"])
        product_id = self.kwargs["pk"]
        product = Product.objects.get(id=product_id)
        print(product)
        YOUR_DOMAIN = "http://127.0.0.1:8000"  # change in production
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[
                {
                    'price_data': {
                        'currency': 'usd',
                        'unit_amount': product.price,
                        'product_data': {
                            'name': product.name,
                        },
                    },
                    'quantity': 1
                },
            ],
            metadata={
               "product_id": product.id 
            },
            mode='payment',
            success_url=YOUR_DOMAIN + '/success/',
            cancel_url=YOUR_DOMAIN + '/cancel/',
        )
        return JsonResponse({
            'id': checkout_session.id

        })



@csrf_exempt
def strip_webhook(request):
 
 payload = request.body
 sig_header = request.META['HTTP_STRIPE_SIGNATURE']
 event = None
 print("test")
 try:
    event = stripe.Webhook.construct_event(
       payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
    )
 except ValueError as e:
    # Invalid payload
    return HttpResponse(status=400)
 except stripe.error.SignatureVerificationError as e:
    # Invalid signature
    return HttpResponse(status=400)
 print(event)
 if event['type'] == 'checkout.session.completed':

    # Retrieve the session. If you require line items in the response, you may include them by expanding line_items.
    session = stripe.checkout.Session.retrieve(
      event['data']['object']['id'],
      expand=['line_items'],
    )
    customer_email = session["customer_details"]["email"] 
    product_id = session["metadata"]["product_id"]
    order_data = session["line_items"]["data"]
    payment_method_type= session["payment_method_types"][0]
    payment_status = session["payment_status"]
    order_status = session["status"]
    print(
        product_id,
        customer_email,
        payment_method_type,
        payment_status,
        order_status)
    # for product in order_data.values():
    #    product_total_amount = product["amount_total"]
    # product = Product.objects.get(id= product_id) 
    save_order_details=OrderDetails(product_id = product_id,
                 customer_email=customer_email,
                 payment_method_type=payment_method_type,
                 payment_status=payment_status,
                 order_status=order_status,
                 jsonResonse=session)
    save_order_details.save()
    send_mail(
       subject="here is your order details on AAA translate",
       message="Thanks for the purchase, here is the order details {product.url}",
       recipient_list=[customer_email],
       from_email="AAAtranslate@gmail.com"
    )
    #print(session)
    ##dump session data into json file and store path of file in db
    # line_items = session.line_items
    # Fulfill the purchase...
    # fulfill_order(line_items)
 return HttpResponse(status=200)
 
