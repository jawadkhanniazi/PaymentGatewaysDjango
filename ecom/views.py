from django.shortcuts import render, redirect
from django.urls import reverse
from paypal.standard.forms import PayPalPaymentsForm
from django.conf import settings
import uuid
import requests
from django.contrib import messages
from .models import ProductDeatils
from django.utils.datastructures import MultiValueDictKeyError
# Create your views here.

def home(request):
    # print('\n',request.GET)
    # product_ordered_by_customer = request.GET.
    # from pdb import set_trace
    # set_trace()
    ##getting the ID of product bigng orderd by the customer
    product_id = int([k for k in request.GET.keys()][0])
    ##details of product will be fetched from BD based on the ID of product
    product_details = ProductDeatils.objects.get(id=product_id)
    
    host = request.get_host()
    #print("host",host)
    paypal_dict = paypal_dict = {
        'business': settings.PAYPAL_RECEIVER_EMAIL,
        'amount': product_details.price,
        'item_name': product_details.name,
        'invoice': str(uuid.uuid4()),
        'currency_code': 'USD',
        'notify_url': f'http://{host}{reverse("paypal-ipn")}',
        'return_url': f'http://{host}{reverse("paypal-return")}',
        'cancel_return': f'http://{host}{reverse("paypal-cancel")}',
    }
    #print('\ndict',paypal_dict)
    form = PayPalPaymentsForm(initial= paypal_dict)
    context = {
        'form':form,
        'name': product_details.name,
        'price': product_details.price
        }
    #print('form',context)
    return render(request,'home.html',context)

def paypal_return(request):
    print('\nsuccess page request data:',request)
    messages.success(request,"you have successfully made a payment")
    return render(request,'compledOrder.html')
    # return redirect('home')

def paypal_cancel(request):
    messages.error(request,"your order has been canceled have successfully made a payment")
    return redirect('home')

def productDeatils(request):
    product_details = ProductDeatils.objects.all()
    data = {
        'product_details':product_details
    }
    
    return render(request,'products.html',data)