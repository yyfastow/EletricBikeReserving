import localflavor
from django import forms
from localflavor.us.forms import USPhoneNumberField, USStateField, USZipCodeField


def must_be_empty(value):
    if value:
        raise forms.ValidationError('is not empty')


class OrderForm(forms.Form):
    name = forms.CharField()
    email = forms.EmailField()
    verify_email = forms.EmailField(label="Please verify your email address")
    phone = USPhoneNumberField()
    """phone = forms.RegexField(
        regex=r'^\+?1?\d{10,.15}$',
        error_message=(
            "Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
        )
    )"""
    state = USStateField()
    city = forms.CharField(max_length=25)
    state2 = localflavor.us.forms.USStateSelect()
    address = forms.CharField(max_length=100)
    zip = USZipCodeField()
    # number = CreditCardField(required = True, label = "Card Number")
    # expiration = CCExpField(required = True, label = "Expiration")
    # ccv_number = forms.IntegerField(required = True, label = "CCV Number",
    #    max_value = 9999, widget = forms.TextInput(attrs={'size': '4'}))

    honeypot = forms.CharField(required=False,
                               widget=forms.HiddenInput,
                               label="leave empty",
                               validators=[must_be_empty],
                               )
#    class Meta:
#        model = models.Bikes

    def clean(self):
        cleaned_data = super().clean()
        name = cleaned_data.get('name')
        verify = cleaned_data.get('verify_email')
        email = cleaned_data.get('email')
        phone = cleaned_data.get('phone1')
        # phone = cleaned_data.get('phone')
        state = cleaned_data.get('state')
        city = cleaned_data.get('city')
        address = cleaned_data.get('address')
        zip = cleaned_data.get('zip')

        if email != verify:
            raise forms.ValidationError(
                "You need to enter the same email in both fields"
            )


