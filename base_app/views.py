from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from django.views.generic import ListView, DetailView
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import authenticate, login, logout
from .models import *
from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.forms import ModelForm
from django.contrib.auth.password_validation import validate_password


# Create your views here.
class TruckListView(ListView):
    model = Truck
    template_name = 'base_app/truck_list_view.html'
    context_object_name = 'trucks'

    def get_queryset(self):
        return Truck.objects.all()

class TruckDetailView(DetailView):
    model = Truck
    context_object_name = 'truck'
    template_name = 'base_app/truckdetails.html'


def loginView(request):
    if request.method == "GET":
        return render(request, "base_app/login.html")
    elif request.method == "POST":
        usr = User.objects.get(email=request.POST['email'])
        if usr is None:
            return redirect('main_page')
        usr_name = usr.username
        user = authenticate(username=usr_name, password=request.POST['password'])
        if user is not None:
            login(request, user)
            messages.info(request, 'Successfully logged in')
            return redirect('main_page')
        else:
            messages.info(request, 'Invalid username and password')
            return redirect('main_page')


def registerView(request):
    if request.method == "GET":
        return render(request, "base_app/signup.html")
    elif request.method == 'POST':
        if request.POST['password1'] != request.POST['password2']:
            messages.error(request, "Passwords don't match")
            return render(request, 'base_app/signup.html')
        else:
            try:
                user_exists = User.objects.get(email=request.POST['email'])
            except Exception as e:
                print(e)
                user_exists = None
            if user_exists:
                messages.error(request, 'There already exists a user with the given email')
            elif user_exists == None:
                password = request.POST.get('password2')
                user = User.objects.create_user(
                    username=request.POST['email'],
                    email=request.POST['email'],
                    password=password,
                    first_name=request.POST['first_name'],
                    last_name=request.POST['last_name']
                )

                if request.POST['user-type'] == 'CLIENT':
                    client = Client.objects.create(user=user, phone=request.POST['phone'],
                                                   aadhar_id=request.POST['aadhar'])
                    messages.success(request, 'You have been successfully registered as a client.Happy hiring')
                    return render(request, 'base_app/index.html')
                elif request.POST['user-type'] == 'OWNER':
                    owner = Owner.objects.create(user=user, phone=request.POST['phone'],
                                                 aadhar_id=request.POST['aadhar'])
                    messages.success(request,
                                     'You have been successfully registered as a truck Owner. LogIn and Add your Truck')
                    return render(request, 'base_app/index.html')


class TruckCreationForm(ModelForm):
    class Meta:
        model = Truck
        exclude = ('is_requested', 'is_rented',)


@login_required(login_url='login')
def create_truck(request):
    if request.method == 'GET':
        return render(request, 'base_app/truckform.html')
    elif request.method == 'POST':
        data = request.POST.copy()
        data['owner'] = request.user.owner
        populated_form = TruckCreationForm(data, request.FILES)
        print(populated_form)
        print(populated_form.errors)
        if populated_form.is_valid():
            populated_form.save()
            messages.success(request, 'Truck Saved successfully')
            return render(request, 'base_app/index.html')
        else:
            messages.error(request, 'Please re-enter the form')
            return render(request, 'base_app/truckform.html')


@login_required(login_url='login')
def logOut(request):
    logout(request)
    messages.success(request, 'succesfully logged out')
    return render(request, 'base_app/index.html')


@login_required(login_url='login')
def truckDelete(request):
    if request.method == 'GET':
        owner = request.user.owner
        truck = Truck.objects.get(owner=owner)
        context = {'truck': truck}
        return render(request, 'base_app/truck_delete_list.html', context)


@login_required(login_url='login')
def create_truck_rent(request, pk):
    if request.method == 'POST':
        from_date = request.POST.get('from_date')
        to_date = request.POST.get('to_date')
        from_date = datetime.strptime(from_date, '%Y-%m-%d').date()
        to_date = datetime.strptime(to_date, '%Y-%m-%d').date()
        truck = Truck.objects.get(id=pk)
        truck.is_requested = True
        truck.save()
        TruckRent.objects.create(client_required_time=from_date, client_drop_time=to_date, truck=truck,
                                 user=request.user.client)
        messages.success(request, 'Your request has been successfully sent. Please await confirmation')
        return redirect('main_page')


@login_required(login_url='login')
def delete_truck_view(request, pk):
    truck = Truck.objects.get(id=pk)
    owner = request.user.owner
    if truck.owner == owner:
        truck.delete()
        messages.success(request, "truck deleted successfully")
    else:
        messages.error(request, "error occured try again later")
    return redirect('main_page')


@login_required(login_url='login')
def truckRequest(request):
    owner = request.user.owner
    truck_rents = owner.truck.truckrent_set.all()
    context = {'truck_rents': truck_rents}
    return render(request, 'base_app/truck_request.html', context)


@login_required(login_url='login')
def cilentRequest(request):
    truckrents = request.user.client.truckrent_set.all()
    context = {'truckrents': truckrents}
    print(request.user.client)
    return render(request, 'base_app/client_request.html', context)


@login_required(login_url='login')
def truck_rent_accept(request, id):
    truck_rent = TruckRent.objects.get(id=id)
    truck_rent.is_verified = True
    truck = truck_rent.truck
    truck.is_rented = True
    truck.save()
    truck_rent.save()
    messages.success(request, 'Your acknowledgement for the request has been successfully recorded')
    return redirect(truckRequest)


@login_required(login_url='login')
def truck_rent_reject(request, id):
    truck_rent = TruckRent.objects.get(id=id)
    truck_rent.is_rejected = True
    truck_rent.save()
    messages.success(request, 'Your rejection for the request has been successfully recorded')
    return redirect(truckRequest)
