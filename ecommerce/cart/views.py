
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from shop.models import Good  # Adjust the import to match your Good model
from .cart import Cart
from .forms import CartAddGoodForm

def cart_add(request, good_id):
    cart = Cart(request)
    good = get_object_or_404(Good, id=good_id)
    form = CartAddGoodForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(good=good, quantity=cd['quantity'], update_quantity=cd['update'])
        messages.success(request, 'Good added to cart successfully!')
    return redirect(request.META.get('HTTP_REFERER', '/'))

def cart_remove(request, good_id):
    cart = Cart(request)
    good = get_object_or_404(Good, id=good_id)
    cart.remove(good)
    return redirect('cart:cart_detail')

def cart_detail(request):
    cart = Cart(request)
    return render(request, 'cart/detail.html', {'cart': cart})
