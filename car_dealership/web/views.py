from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect


# Create your views here.
from .forms import UserForm


def index(request):
    return render(request, 'web/index.html')


def login_user(request):
    if request.user.is_authenticated:
        return redirect('web:home')
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect('web:home')
            else:
                return render(request, 'web/login.html', {'error_message': 'Your account has not been activated!'})
        else:
            return render(request, 'web/login.html', {'error_message': 'Invalid login'})
    return render(request, 'web/login.html')


def register(request):
    if request.user.is_authenticated:
        return redirect('web:home')
    uform = UserForm(request.POST or None)
    if uform.is_valid() and pform.is_valid():
        user = uform.save(commit=False)
        username = uform.cleaned_data['username']
        password = uform.cleaned_data['password']
        user.set_password(password)
        user.save()
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect('web:home')

    context = {
        "uform": uform,
    }

    return render(request, 'web/register.html', context)


def cars(request):
    return render(request, 'web/cars.html')
