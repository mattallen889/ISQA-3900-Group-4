from django import forms
class CartAddProductForm(forms.Form):
    def __init__(self, *args, **kwargs):
        try: #if choices for quantity drop-down provided
            mychoices = kwargs.pop('my_choices')
            super(CartAddProductForm, self).__init__(*args, **kwargs)
            self.fields["quantity"] = forms.TypedChoiceField(choices=mychoices,
                coerce=int)
        except: #use default of 21 if choices not provided
            super(CartAddProductForm, self).__init__(*args, **kwargs)
            self.fields["quantity"] = forms.TypedChoiceField(choices=[(i, str(i)) for i in range(1, 21)],
                                                             coerce=int)

    update = forms.BooleanField(required=False,
                                    initial=False,
                                    widget=forms.HiddenInput)





