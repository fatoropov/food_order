from django import forms


PRODUCT_QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 21)]


class CartAddDishForm(forms.Form):
    quantity = forms.IntegerField(
        widget=forms.NumberInput(attrs={'class': 'bootstrap-input-spinner',
                                        'value': 1,
                                        'min': 1,
                                        'max': 20,
                                        'step': 1}),
        required=False,
        initial=1,
        label="")
    override = forms.BooleanField(required=False,
                                  initial=False,
                                  widget=forms.HiddenInput)
