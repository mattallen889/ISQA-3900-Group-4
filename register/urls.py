from django.urls import path
from . import views

app_name = 'register'

urlpatterns = [
    path('', views.register, name='register'),
    path('registrationError/<int:regErrorID>', views.registerErrorHandle, name='registerErrorHandle'),
    path('signup/', views.signup, name='signup'),
]