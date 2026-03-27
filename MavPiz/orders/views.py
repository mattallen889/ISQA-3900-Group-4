from django.urls import reverse
from django.shortcuts import render, redirect, get_object_or_404
from .models import OrderItem, Order, Product
from .forms import OrderCreateForm
from cart.cart import Cart
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.core.mail import send_mail


@staff_member_required
def admin_order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request,
                  'admin/orders/order/detail.html',
                  {'order': order})


def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            if request.user.is_authenticated:
                order.user = request.user
            order.save()

            order_items_text = []
            total_cost = 0

            for item in cart:
                OrderItem.objects.create(order=order,
                                         product=item['product'],
                                         price=item['price'],
                                         quantity=item['quantity'])
                line_total = item['price'] * item['quantity']
                total_cost += line_total
                order_items_text.append(f"{item['quantity']} x {item['product'].name} - ${line_total:.2f}")
                item['product'].quantity = item['product'].quantity - item['quantity']
                item['product'].save()
            send_mail(subject=f"Your Maverick's Pizza Order was Received! #{order.id}",
                message=(
                    f"Thank you for your order, {order.first_name} {order.last_name}!\n\n"
                    f"Your order number is {order.id}.\n\n"
                    f"Order summary:\n"
                    + "\n".join(order_items_text)
                    + f"\n\nTotal: ${total_cost:.2f}\n\n"
                    f"Thank you <3"
                ),
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[order.email],
                fail_silently=False,)


            cart.clear()
            request.session['order_id'] = order.id

            return render(request, 'orders/order/created.html', {'order_id': order.id})
    else:
        form = OrderCreateForm()
    return render(request,
                  'orders/order/create.html',
                  {'cart': cart, 'form': form})


@login_required
def user_orders(request):
    orders = Order.objects.filter(user=request.user)
    return render(request, 'orders/order/my_orders.html', {'orders': orders})