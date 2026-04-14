from django.urls import reverse
from django.shortcuts import render, redirect, get_object_or_404
from .models import OrderItem, Order, Product
from .forms import OrderCreateForm, ManualOrderItemForm
from cart.cart import Cart
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.core.mail import send_mail

from datetime import datetime

def manage_customer_orders(request):
    if request.user.is_authenticated and request.user.is_staff:
        customerOrders = Order.objects.all()
        return render(request, 'admin/manageCustomerOrders.html', {'customerOrders': customerOrders})
    else:
        return redirect('/')

def view_customer_order_details(request, orderID):
    if request.user.is_authenticated and request.user.is_staff:
        order = Order.objects.get(id=orderID)
        orderItems = OrderItem.objects.filter(order=order)
        return render(request, 'admin/viewCustomerOrderDetails.html', {'order': order, 'orderItems': orderItems})
    else:
        return redirect('/')

def finish_order(request, orderID):
    if request.user.is_authenticated and request.user.is_staff:
        order = Order.objects.get(id=orderID)
        order.delete()
        return redirect('/orders/manage_customer_orders/')
    else:
        return redirect('/')

@staff_member_required
def admin_order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request,
                  'admin/orders/order/detail.html',
                  {'order': order})

def paymentPageSubmit(request, orderID):
    order = Order.objects.get(id=orderID)
    order.paid = True
    order.save()
    return render(request, 'orders/order/created.html', {'order_id': order.id})

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
                OrderItem.objects.create(
                    order=order,
                    product=item['product'],
                    price=item['price'],
                    quantity=item['quantity']
                )
                line_total = item['price'] * item['quantity']
                total_cost += line_total
                order_items_text.append(f"{item['quantity']} x {item['product'].name} - ${line_total:.2f}")

                # reduce the number of items in inventory based on this sale
                item['product'].quantity = item['product'].quantity - item['quantity']
                item['product'].save()

            send_mail(
                subject=f"Your Maverick's Pizza Order was Received! #{order.id}",
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
                fail_silently=False,
            )

            # clear the cart
            cart.clear()
            # set the order in the session
            request.session['order_id'] = order.id

            return render(request, 'orders/order/payment_Page.html', {'orderID': order.id, 'price': f'${total_cost}'})
    else:
        form = OrderCreateForm()

    # Get the current time
    currTime = datetime.now()

    currentTime = str(currTime).split(' ')[1].split('.')[0].split(':')
    hour24 = currentTime[0]
    hour = hour24
    hour24 = int(hour24)
    minute = currentTime[1]
    dayDivision = 'AM'
    hourConversion = {"0": "12",
                      "00": "12",
                      "13": "1",
                      "14": "2",
                      "15": "3",
                      "16": "4",
                      "17": "5",
                      "18": "6",
                      "19": "7",
                      "20": "8",
                      "21": "9",
                      "22": "10",
                      "23": "11"}

    # Convert current time into 12-hour format
    if hour == "00":
        hour = hourConversion["00"]
        dayDivision = 'AM'
    elif hour in hourConversion:
        hour = hourConversion[hour]
        dayDivision = 'PM'
    else:
        pass

    increments = []

    # Find twelve 30-min increments
    while (len(increments) < 12):
        if (int(hour) + 1) < 12:
            increments.append(f"{str(int(hour) + 1)}:30 {dayDivision}")
            hour = str(int(hour) + 1)
        elif (int(hour) + 1) == 12:
            dayDivision = 'PM' if dayDivision == 'AM' else 'AM'
            increments.append(f"{str(int(hour) + 1)}:30 {dayDivision}")
            hour = str(int(hour) + 1)
        elif (int(hour) + 1) > 12:
            hour = hourConversion[str(int(hour) + 1)]
            increments.append(f'{hour}:30 {dayDivision}')
        else:
            pass

    return render(request,
                  'orders/order/create.html',
                  {'cart': cart, 'form': form, 'currentHour': hour, 'currentMinute': minute, 'dayDivision': dayDivision,
                   'increments': increments})


@login_required
def user_orders(request):
    orders = Order.objects.filter(user=request.user)
    return render(request, 'orders/order/my_orders.html', {'orders': orders})

@staff_member_required
def add_manual_order(request):
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save()
            return redirect('orders:add_manual_order_items', orderID=order.id)
    else:
        form = OrderCreateForm()
    return render(request, 'admin/addManualOrder.html', {'form': form})

@staff_member_required
def add_manual_order_items(request, orderID):
    order = get_object_or_404(Order, id=orderID)
    if request.method == 'POST':
        form = ManualOrderItemForm(request.POST)
        if form.is_valid():
            order_item = form.save(commit=False)
            order_item.order = order
            order_item.price = order_item.product.price
            order_item.save()
            return redirect('orders:add_manual_order_items', orderID=order.id)
    else:
        form = ManualOrderItemForm()
    order_items = OrderItem.objects.filter(order=order)

    return render(request, 'admin/addManualOrderItems.html', {
        'order': order,
        'form': form,
        'order_items': order_items
    })

@staff_member_required
def delete_order(request, orderID):
    order = get_object_or_404(Order, id=orderID)
    order.delete()
    return redirect('orders:manage_customer_orders')