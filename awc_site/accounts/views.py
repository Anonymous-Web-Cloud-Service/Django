from django.shortcuts import render, redirect
from accounts.forms import UserForm, LoginForm
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import login as auth_login, authenticate, logout as auth_logout


def sign_up(request):
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        if user_form.is_valid():
            user_form.save()
            return render(request, 'accounts/sign_up_done.html', {'nickname': user_form['nickname'].value()})
        else:
            print(user_form.errors)

    else:
        user_form = UserForm()
    return render(request, 'accounts/sign_up.html', {'user_form': user_form})


def login(request):
    if request.method == "POST":
        login_form = LoginForm(data=request.POST)
        email = login_form['email'].value()
        password = login_form['password'].value()

        member = authenticate(username=email, password=password)
        if member is not None:
            auth_login(request, member)
            return render(request, 'main.html', {'user': member})
        else:
            return HttpResponse('로그인 실패입니다.')

    else:
        login_form = LoginForm()
        return render(request, 'accounts/login.html', {'login_form': login_form})


# 로그아웃
def logout(request):
    auth_logout(request)
    return redirect('/')


# 메인화면 표시
def index(request):
    return render(request, 'main.html', {})


def shared_main(request):
    return render(request, 'main.html')
