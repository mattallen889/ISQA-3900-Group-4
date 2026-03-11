from django.urls import path
from . import views

app_name = 'shop'

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('<int:id>/', views.product_detail, name='product_detail'),
    path('<slug:category_slug>/', views.product_list, name='product_list_by_category'),

#added code for base.html connection by Nate
    path('registration/login/', views.login, name='login'), # Points to your login view
    path('registration/logout/', views.user_logout, name='logout'),

    path('registration/logged_out/', views.logged_out, name='logged_out'), # Points to sign_up
    path('catalog/profile/', views.profile, name='profile'), # Points to profile
]