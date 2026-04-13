from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('create/', views.order_create, name='order_create'),
    path('admin/order/<int:order_id>/', views.admin_order_detail, name='admin_order_detail'),
    path('my-orders/', views.user_orders, name='user_orders'),
    path('makepayment/<int:orderID>', views.paymentPageSubmit, name='paymentPageSubmit'),
    path('manage_customer_orders/', views.manage_customer_orders, name='manage_customer_orders'),
    path('view_customer_order_details/<int:orderID>', views.view_customer_order_details, name='view_customer_order_details'),
    path('finish_order/<int:orderID>', views.finish_order, name='finish_customer_orders'),
]