import random
import stripe
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseRedirect
from django.shortcuts import render

from products.models import Product
from .models import Purchase
from cfehome.env import config

STRIPE_SECRET_KEY = config("STRIPE_SECRET_KEY", default=None)
stripe.api_key = STRIPE_SECRET_KEY

BASE_ENDPOINT= config("BASE_ENDPOINT", default="http://127.0.0.1:8000")

def purchase_start_view(request):
    if not request.method == "POST":
        return HttpResponseBadRequest()
    if not request.user.is_authenticated:
        return HttpResponseBadRequest()
    handle = request.POST.get("handle")
    obj = Product.objects.get(handle=handle)
    strip_price_id = obj.strip_price_id
    if stripe_price_id is None:
        return HttpResponseBadRequest() 
    purchase = purchase = Purchase.objects.create(user=request.user, product=obj)
    request.session['purchase_id'] = purchase.id
    success_url = f"{base_endpoint}/purchases/success/"
    cancel_url = f"{base_endpoint}/purchases/stopped/"
    checkout_session = stripe.checkout.Session.create(
        line_items = [
            {
                "price": stripe_price_id,
                "quantity": 1,
            }
        ],
        mode="payment",
        success_url=success_url,
        cancel_url=cancel_url
    )

    return HttpResponse("Started")


def purchase_success_view(request):
    purchase_id = request.session.get("purchase_id")
    if purchase_id:
        purchase = Purchase.objects.get(id=purchase_id)
        purchase.completed = True
        purchase.save()
        del request.session['purchase_id']
        return HttpResponseRedirect(purchase.product.get_absolute_url())
    return HttpResponse(f"Finished {purchase_id}")


def purchase_stopped_view(request):
    return HttpResponse("Stopped")