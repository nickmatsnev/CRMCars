from django.shortcuts import *
from django.contrib.auth import login, logout
from portal.controllers.forms import *


def sign_in(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['username'], password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('clients_list')
                else:
                    return HttpResponse('Аккаунт не активен')
            else:
                return HttpResponse('Неверная пара логин\пароль')
    else:
        form = LoginForm()
    return render(request, 'signin.html', {'form': form})



def sign_up(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('clients_list')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})

def sign_out(request):
   logout(request)
   return redirect('signin')