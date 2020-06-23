from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User, Quote
import bcrypt
# Create your views here.
def index(request):
    return render(request, "index.html")

def dashboard(request):
    user = User.objects.get(id=request.session['userid'])
    favorites = Quote.objects.filter(favorites=user)
    print(favorites)
    context = {
        "user": User.objects.get(id=request.session['userid']),
        "all_quotes": Quote.objects.exclude(favorites=user),
        "user_favorites": favorites
    }
    return render(request, "quotes.html", context)

def register_user(request): 
    errors = User.objects.validator(request.POST)
    password = request.POST['password']
    pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request,value)
        return redirect("/")
    else: 
        User.objects.create(email=request.POST['email'], name=request.POST['name'], password=pw_hash)
        user = User.objects.filter(email=request.POST['email'])
        if user: 
            logged_user = user[0]
            request.session['userid'] = logged_user.id
            return redirect('/quotes')
        return reidrect('/quotes')

def login_user(request):
    errors  = User.objects.validatorLogin(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request,value)
        return redirect("/")
    else: 
        user = User.objects.filter(email=request.POST['email_login'])
        logged_user = user[0]
        request.session['userid'] = logged_user.id
        return redirect("/quotes")

def contribute_quote(request):
    errors = Quote.objects.quoteValidator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request,value)
        return redirect("/quotes")
    else:
        user = request.session['userid']
        ID = User.objects.get(id=user)
        Quote.objects.create(author=request.POST['author'], message=request.POST['message'], user=ID)
        return redirect('/quotes')

def user_page(request, num):
    user = User.objects.get(id=num)
    context = {
        "user": user,
        "user_quotes": Quote.objects.filter(user=user),
        "count": Quote.objects.filter(user=user).count()
    }
    return render(request, "user_page.html", context)

def edit_page(request,num):
    context = {
        "quote": Quote.objects.get(id=num),
    }
    return render(request, "edit_quote.html", context)

def edit_quote(request, num):
    errors = Quote.objects.quoteValidator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request,value)
        return redirect(f"/quotes/{num}")
    else:
        quote = Quote.objects.get(id=num)
        quote.author = request.POST['author']
        quote.message = request.POST['message']
        quote.save()
    return redirect("/quotes")

def delete_quote(request,num):
    quote = Quote.objects.get(id=num)
    quote.delete()
    return redirect("/quotes")

def add_to_fave(request,num):
    quote = Quote.objects.get(id=num)
    user = User.objects.get(id=request.session["userid"])
    quote.favorites.add(user)
    return redirect("/quotes")

def remove_from_fave(request, num):
    quote = Quote.objects.get(id=num)
    user = User.objects.get(id=request.session["userid"])
    quote.favorites.remove(user)
    return redirect("/quotes")

def logout_user(request):
    del request.session['userid']
    return redirect('/')


