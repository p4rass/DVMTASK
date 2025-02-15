from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Bus, Passenger, Wallet

class UserRegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']

class UserLoginForm(AuthenticationForm):
    pass

class BusForm(forms.ModelForm):
    class Meta:
        model = Bus
        fields = '__all__'

class PassengerForm(forms.ModelForm):
    class Meta:
        model = Passenger
        fields = ['name', 'age', 'gender']

class WalletForm(forms.ModelForm):
    class Meta:
        model = Wallet
        fields = ['balance']

class TicketBookingForm(forms.Form):
    source = forms.ChoiceField(label="Source")
    destination = forms.ChoiceField(label="Destination")
    date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), label="Date")
    num_tickets = forms.IntegerField(min_value=1, label="Number of Tickets")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        sources = Bus.objects.values_list('source', flat=True).distinct()
        destinations = Bus.objects.values_list('destination', flat=True).distinct()
        self.fields['source'].choices = [(src, src) for src in sources]
        self.fields['destination'].choices = [(dst, dst) for dst in destinations]