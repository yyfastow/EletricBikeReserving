from datetime import datetime

from django import forms
from django.contrib.auth.models import User

from Bikes import models

# TODO: use stripe to charge, need to make account with them
# I wont do this unless this site really becomes something that charged people
# for I cant play around with credit charges.


def get_cc_type(number):
    """
    Gets credit card type given number. Based on values from Wikipedia page/
    "Credit card number".
    http://en.wikipedia.org/w/index.php?title=Credit_card_number
       """
    number = str(number)
    # group checking by ascending length of number
    if len(number) == 13:
        if number[0] == "4":
            return "Visa"
    elif len(number) == 14:
        if number[:2] == "36":
            return "MasterCard"
    elif len(number) == 15:
        if number[:2] in ("34", "37"):
            return "American Express"
    elif len(number) == 16:
        if number[:4] == "6011":
            return "Discover"
        if number[:2] in ("51", "52", "53", "54", "55"):
            return "MasterCard"
        if number[0] == "4":
            return "Visa"
    return "Unknown"


def must_be_empty(value):
    if value:
        raise forms.ValidationError('is not empty')


class PasswordForm(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput)
    verify_password = forms.CharField(max_length=20, label="Please verify your password", widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        verify_password = cleaned_data.get('verify_password')

        if password != verify_password:
            raise forms.ValidationError(
                "You need to enter the same password in password and Verity Password Fields"
            )

        if User.objects.filter(password=password).exists():
            raise forms.ValidationError(
                "This name is allready used by another costomer"
            )


class OrderForm(forms.ModelForm):

    class Meta:
        model = models.Order
        fields = [
            'name',
            'phone',
            'email'
        ]

    verify_email = forms.EmailField(max_length=254, label="Please verify your email address")
    honeypot = forms.CharField(required=False,
                               widget=forms.HiddenInput,
                               label="leave empty",
                               validators=[must_be_empty],
                               )

    def clean(self):
        cleaned_data = super().clean()
        name = cleaned_data.get('name')
        verify = cleaned_data.get('verify_email')
        email = cleaned_data.get('email')
        phone = cleaned_data.get('phone')

        if email != verify:
            raise forms.ValidationError(
                "You need to enter the same email in both fields"
            )


class BillingForm(forms.ModelForm):
    class Meta:
        model = models.Billing
        fields = ['state', 'city', 'address', 'zip']

    def clean(self):
        cleaned_data = super().clean()
        state = cleaned_data.get('state')
        city = cleaned_data.get('city')
        address = cleaned_data.get('address')
        zip = cleaned_data.get('zip')


class CardForm(forms.ModelForm):
    ccv_number = forms.IntegerField(widget=forms.TextInput(attrs={'size': '4'}))
    expiration = forms.DateField(widget=forms.SelectDateWidget)
    class Meta:
        model = models.Card
        fields = ['number',
            'expiration',
            'ccv_number',
            ]

    def clean(self):
        cleaned_data = super().clean()
        number = cleaned_data.get('number')
        expiration = cleaned_data.get('expiration')
        ccv_number = cleaned_data.get('ccv_number')

        if expiration == datetime.now():
            raise forms.ValidationError(
                "Credit card can not be expired"
            )

        if number and (len(str(number)) < 13 or len(str(number)) > 16):
            raise forms.ValidationError("Please enter in a valid " + \
                                        "credit card number.")
        elif get_cc_type(number) not in ("Visa", "MasterCard",
                                         "American Express"):
            raise forms.ValidationError("Please enter in a Visa, " + \
                                        "Master Card, or American Express credit card number.")

        if ccv_number and len(str(ccv_number)) > 4:
            raise forms.ValidationError(
                "Make sure to add your ccv number no more then 4 digits!"
            )

class SelectionForm(forms.Form):
    card = forms.ModelChoiceField(queryset=models.Card.objects.all(),
                                    empty_label=None)
    billing = forms.ModelChoiceField(queryset=models.Billing.objects.all(),
                                    # widget=forms.RadioSelect(),
                                    empty_label=None)

    def clean(self):
        cleaned_data = super().clean()
        card = cleaned_data.get('card')
        billing = cleaned_data.get('billing')


class BillSelectionForm(forms.Form):
    billing = forms.ModelChoiceField(queryset=models.Billing.objects.all(),
                                     empty_label=None)

    def clean(self):
        cleaned_data = super().clean()
        billing = cleaned_data.get('billing')


class CardSelectionForm(forms.Form):
    card = forms.ModelChoiceField(queryset=models.Card.objects.all(),
                                    empty_label=None)

    def clean(self):
        cleaned_data = super().clean()
        card = cleaned_data.get('card')


class LoginForm(forms.Form):
    name = forms.CharField(max_length=100, label="name  ")
    email = forms.EmailField(max_length=254, label="Email:  ")
    password = forms.CharField(widget=forms.PasswordInput)
    honeypot = forms.CharField(required=False,
                               widget=forms.HiddenInput,
                               label="leave empty",
                               validators=[must_be_empty],
                               )

    def clean(self):
        cleaned_data = super().clean()
        name = cleaned_data.get('name')
        email = cleaned_data.get('email')
        password = cleaned_data.get('password')


class MessageForm(forms.ModelForm):
    class Meta:
        model = models.Message
        fields = ['message']



class AmountForm(forms.Form):
    amount = forms.IntegerField()

    def clean(self):
        cleaned_data = super().clean()
        amount = cleaned_data.get('amount')

        if amount < 1:
            raise forms.ValidationError(
                "You cant order zero or Negative amounts"
            )



BillingFormSet = forms.modelformset_factory(
    models.Billing,
    form=BillingForm,
    extra=1
)

CardFormSet = forms.modelformset_factory(
    models.Card,
    form=CardForm,
    extra=0,
)

BillingInlineFormSet = forms.inlineformset_factory(
    models.Order,
    models.Billing,
    extra=0,
    fields=('state', 'city', 'address', 'zip'),
    formset=BillingFormSet,
)

CardInlineFormSet = forms.inlineformset_factory(
    models.Order,
    models.Card,
    extra=1,
    fields=('number', 'expiration', 'ccv_number',),
    formset=CardFormSet,
)

"""def clean(self):
        cleaned_data = super().clean()
        billings = cleaned_data.get('billings')
        cards = cleaned_data.get('cards')
"""
