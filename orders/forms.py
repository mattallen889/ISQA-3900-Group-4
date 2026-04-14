from django import forms
from .models import Order, OrderItem

# Create a tuple list of times (Value saved to DB, Human-readable name)
TIME_CHOICES = [
    ('9:00 AM', '9:00 AM'), ('9:30 AM', '9:30 AM'),
    ('10:00 AM', '10:00 AM'), ('10:30 AM', '10:30 AM'),
    ('11:00 AM', '11:00 AM'), ('11:30 AM', '11:30 AM'),
    ('12:00 PM', '12:00 PM'), ('12:30 PM', '12:30 PM'),
    ('1:00 PM', '1:00 PM'), ('1:30 PM', '1:30 PM'),
    ('2:00 PM', '2:00 PM'), ('2:30 PM', '2:30 PM'),
    ('3:00 PM', '3:00 PM'), ('3:30 PM', '3:30 PM'),
    ('4:00 PM', '4:00 PM'), ('4:30 PM', '4:30 PM'),
    ('5:00 PM', '5:00 PM'), ('5:30 PM', '5:30 PM'),
    ('6:00 PM', '6:00 PM'), ('6:30 PM', '6:30 PM'),
    ('7:00 PM', '7:00 PM'), ('7:30 PM', '7:30 PM'),
    ('8:00 PM', '8:00 PM'), ('8:30 PM', '8:30 PM'),
    ('9:00 PM', '9:00 PM'), ('9:30 PM', '9:30 PM'),
    ('10:00 PM', '10:00 PM'), ('10:30 PM', '10:30 PM'),
]

class OrderCreateForm(forms.ModelForm):
    # Added the label="Pickup Time" argument here!
    pickupTime = forms.ChoiceField(
        choices=TIME_CHOICES,
        label='Pickup Time',
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'email', 'address',
                  'postal_code', 'city', 'pickup_date', 'pickupTime']

        widgets = {
            'pickup_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }

class ManualOrderItemForm(forms.ModelForm):   # *** ADDED ***
    class Meta:
        model = OrderItem
        fields = ['product', 'quantity']
        widgets = {
            'product': forms.Select(attrs={'class': 'form-control'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
        }