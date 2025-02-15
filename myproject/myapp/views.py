from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from .models import Bus, Passenger, Booking, Wallet
from .forms import UserRegisterForm, UserLoginForm, BusForm, PassengerForm, WalletForm, TicketBookingForm

def home(request):
    return render(request, 'myapp/home.html')

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            Wallet.objects.create(user=user, balance=0.00)
            login(request, user)
            return redirect('ticket_booking')
    else:
        form = UserRegisterForm()
    return render(request, 'myapp/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('ticket_booking')
    else:
        form = UserLoginForm()
    return render(request, 'myapp/login.html', {'form': form})

@login_required
def ticket_booking(request):
    wallet = Wallet.objects.get_or_create(user=request.user)[0]
    if request.method == 'POST':
        form = TicketBookingForm(request.POST)
        if form.is_valid():
            source = form.cleaned_data['source']
            destination = form.cleaned_data['destination']
            date = form.cleaned_data['date']
            num_tickets = form.cleaned_data['num_tickets']
            buses = Bus.objects.filter(source=source, destination=destination, departure_time__date=date)
            return render(request, 'myapp/ticket_booking.html', {
                'form': form,
                'buses': buses,
                'num_tickets': num_tickets
            })
    else:
        form = TicketBookingForm()
    return render(request, 'myapp/ticket_booking.html', {'form': form})

@login_required
def passenger_details(request, bus_id):
    bus = get_object_or_404(Bus, id=bus_id)
    num_tickets = int(request.GET.get('num_tickets', 1))
    current_passenger = len(request.session.get('passengers', [])) + 1

    if request.method == 'POST':
        form = PassengerForm(request.POST)
        if form.is_valid():
            if 'passengers' not in request.session:
                request.session['passengers'] = []
            request.session['passengers'].append(form.cleaned_data)
            request.session.modified = True

            if current_passenger >= num_tickets:
                return redirect('confirm_booking', bus_id=bus_id)
            else:
                return redirect('passenger_details', bus_id=bus_id)
    else:
        form = PassengerForm()

    return render(request, 'myapp/passenger_details.html', {
        'bus': bus,
        'form': form,
        'num_tickets': num_tickets,
        'current_passenger': current_passenger
    })

@login_required
def confirm_booking(request, bus_id):
    bus = get_object_or_404(Bus, id=bus_id)
    wallet = Wallet.objects.get(user=request.user)
    passengers = request.session.get('passengers', [])
    num_tickets = len(passengers)
    total_fare = bus.fare * num_tickets

    if request.method == 'POST':
        if wallet.balance < total_fare:
            messages.error(request, "Insufficient wallet balance. Add money first.")
            return redirect('add_money')

        booking = Booking.objects.create(
            user=request.user,
            bus=bus,
            num_tickets=num_tickets,
            total_fare=total_fare
        )
        for passenger_data in passengers:
            passenger = Passenger.objects.create(**passenger_data)
            booking.passengers.add(passenger)

        bus.available_seats -= num_tickets
        bus.save()
        wallet.balance -= total_fare
        wallet.save()
        del request.session['passengers']
        return redirect('booking_success', booking_id=booking.id)

    return render(request, 'myapp/confirm_booking.html', {
        'bus': bus,
        'passengers': passengers,
        'total_fare': total_fare,
        'wallet_balance': wallet.balance
    })

@login_required
def booking_success(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    
    wallet = Wallet.objects.get(user=request.user)
    passengers = booking.passengers.all()

    return render(request, 'myapp/booking_success.html', {
        'booking': booking,
        'wallet_balance': wallet.balance,
        'passengers': passengers
    })

@login_required
def add_money(request):
    wallet = Wallet.objects.get(user=request.user)
    if request.method == 'POST':
        form = WalletForm(request.POST, instance=wallet)
        if form.is_valid():
            form.save()
            return redirect('ticket_booking')
    else:
        form = WalletForm(instance=wallet)
    return render(request, 'myapp/add_money.html', {'form': form})

@user_passes_test(lambda u: u.is_superuser)
def admin_dashboard(request):
    buses = Bus.objects.all()
    return render(request, 'myapp/admin_dashboard.html', {'buses': buses})

@user_passes_test(lambda u: u.is_superuser)
def add_bus(request):
    if request.method == 'POST':
        form = BusForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin_dashboard')
    else:
        form = BusForm()
    return render(request, 'myapp/add_bus.html', {'form': form})