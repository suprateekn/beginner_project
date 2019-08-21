from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import login, logout
from django.shortcuts import render, redirect

from chat_app.forms import SignupForm


def home_page(request):
    if request.method == 'POST':
        logout(request)
        return redirect('login_page')

    return render(request, "home.html")


def login_page(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')

        else:
            context = {"error_msg": 'Incorrect Credentials'}
            template = "login.html"
            return render(request, template, context)

    else:
        template = "login.html"
        context = {"title": "LOGIN"}
        return render(request, template, context)


def signup_page(request):
    if request.method == 'POST':
        print(request.FILES)
        form = SignupForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()
            user.UserProfile.profile_pic = form.cleaned_data.get('profile_pic')
            user.save()

            return redirect('login_page')
        else:
            context = {"error_msg": form.error_messages['password_mismatch'], "form": form, 'title': "SIGNUP"}
            return render(request, "signup.html", context)

    else:
        form = SignupForm()
        context = {'form': form, 'title': "SIGNUP"}
        return render(request, "signup.html", context)
