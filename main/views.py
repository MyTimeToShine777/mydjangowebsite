from django.shortcuts import render, redirect
from main.models import Item
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages


# Create your views here.


def homepage(request):
    return render(request, template_name='main/home.html')


def itemspage(request):
    if request.method == 'GET':
        items = Item.objects.filter(owner=None)
        return render(request, template_name='main/items.html', context={'items': items})
    if request.method == 'POST':
        purchased_item = request.POST.get('purchased-item')
        if purchased_item:
            purchased_item_object = Item.objects.get(name=purchased_item)
            purchased_item_object.owner = request.user
            purchased_item_object.save()
            messages.success(
                request, f'congratulations, You just bought {purchased_item_object.name} for {purchased_item_object.price}$')

        return redirect('items')


def registerpage(request):

    if request.method == 'GET':
        return render(request, template_name='main/register.html')

    if request.method == 'POST':

        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(
                request, f'You have registered your account successfuly! Logged in as {user.username}')
            return redirect('home')
        else:
            messages.error(request, form.errors)
            return redirect('register')


def loginpage(request):
    if request.method == 'GET':
        return render(request, template_name='main/login.html')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(
                request, f'You are successfuly! Logged in as {user.username}')
            return redirect('items')
        else:
            messages.error(
                request, 'The username and password you enterd did not match our records. Please double check and try again.')
            return redirect('login')


def logoutpage(request):
    logout(request)
    messages.success(
        request, f'You have been logged out! ')
    return redirect('home')


def orderspage(request):

    return render(request, template_name='main/orders.html')
