from django import forms


class CartAddProductForm(forms.Form):
    # This creates the number input box, defaulting to 1, with a max of 20
    quantity = forms.IntegerField(
        min_value=1,
        max_value=20,
        initial=1,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'style': 'width: 80px;'})
    )

    update = forms.BooleanField(
        required=False,
        initial=False,
        widget=forms.HiddenInput
    )

    def __init__(self, *args, **kwargs):
        # We safely remove 'my_choices' if your views.py is still trying to pass it.
        # This prevents Django from crashing with an "unexpected keyword" error.
        kwargs.pop('my_choices', None)
        super(CartAddProductForm, self).__init__(*args, **kwargs)





