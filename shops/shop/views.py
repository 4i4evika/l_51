from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from .forms import ShopForm
from .models import Shop
from django.utils import timezone
from django.contrib.auth.decorators import login_required


def home(request):
    return render(request, 'shop/home.html')


def signupuser(request):
    if request.method == 'GET':
        return render(request, 'shop/signupuser.html', {'form': UserCreationForm()})
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(
                    request.POST['username'],
                    password=request.POST['password1']
                )
                user.save()
                login(request, user)
                return redirect('currentshops')
            except IntegrityError:
                return render(request, 'shop/signupuser.html',
                              {'form': UserCreationForm(),
                               'error': 'Такое имя пользователя уже существует'})
        else:
            return render(request, 'shop/signupuser.html',
                          {'form': UserCreationForm(),
                           'error': 'Пароли не совпали'})


def loginuser(request):
    if request.method == 'GET':
        return  render(request, 'shop/loginuser.html',
                       {'form': AuthenticationForm()})
    else:
        user = authenticate(request, username=request.POST['username'],
                            password=request.POST['password'])
        if user is None:
            return render(request, 'shop/loginuser.html',
                          {'form': AuthenticationForm(),
                           'error': 'Неверные данные для входа'})
        else:
            login(request, user)
            return redirect('currentshops')

@login_required
def logoutuser(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')


@login_required
def currentshops(request):
    shops = Shop.objects.filter(user=request.user)
    return render(request, 'shop/currentshops.html', {'shops': shops})

@login_required
def createshop(request):
    if request.method == 'GET':
        return render(request, 'shop/createshop.html', {'form': ShopForm()})
    # else:
    #     try:
    #         form = ShopForm(request.POST)
    #         new_shop = form.save(commit=False)
    #         new_shop.user = request.user
    #         new_shop.save()
    #         return redirect('currentshops')
    #     except ValueError:
    #         return render(request, 'shop/createshop.html',
    #                       {'form': ShopForm(),
    #                        'error': 'Переданы неверные данные, попробуйте ещё раз'})


@login_required
def viewshop(request, shop_pk):
    shop = get_object_or_404(Shop, pk=shop_pk)
    form = ShopForm(instance=shop)
    if request.method == 'GET':
        return render(request, 'shop/viewshop.html', {'shop': shop,
                                                                           'form': form})
    else:
        try:
            form = ShopForm(request.POST, instance=shop)
            form.save()
            return redirect('currentshops')
        except ValueError:
            return render(request, 'shop/viewshop.html', {'shop': shop,
                                                          'form': form,
                                                          'error': 'Неверные данные'})

@login_required
def completeshop(request, shop_pk):
    shop = get_object_or_404(Shop, pk=shop_pk, user=request.user)
    if request.method == 'POST':
        shop.date_completed = timezone.now()
        shop.save()
        return redirect('currentshops')


@login_required
def deleteshop(request, shop_pk):
    shop = get_object_or_404(Shop, pk=shop_pk, user=request.user)
    if request.method == 'POST':
        shop.delete()
        return redirect('currentshops')


@login_required
def basketshops(request):
    shops = Shop.objects.filter(user=request.user)
    return render(request, 'shop/currentshops.html', {'shops': shops})