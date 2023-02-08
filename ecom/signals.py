from paypal.standard.models import ST_PP_COMPLETED
from paypal.standard.ipn.signals import valid_ipn_received, invalid_ipn_received
from .models import Order
from django.dispatch import receiver



@receiver(valid_ipn_received)
def valid_ipn_signal(sender, **kwargs):
    print('\nipn valid\n')
    ipn = sender
    if ipn.payment_status == 'Completed':
        Order.objects.create()


@receiver(invalid_ipn_received)
def invalid_ipn_signal(sender, **kwargs):
    print('\nipn in-valid\n')
    ipn = sender
    if ipn.payment_status == 'Completed':
        Order.objects.create()