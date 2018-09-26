from django.shortcuts import render, redirect
from .models import User, Product
from django.contrib import messages

# Create your views here.
def index(request):
    return render(request, "index.html")
def register(request):
    results = User.objects.register(request.POST)
    if isinstance(results, User):
        request.session['User_id'] = results.id
        messages.add_message(request, messages.SUCCESS, 'Welcome, {}'.format(results))
        return redirect('/')
    else:
        for key in results:
            messages.add_message(request, messages.ERROR, results[key])
        return redirect("/")
def login(request):
    results = User.objects.login(request.POST)
    if isinstance(results, User):
        request.session['User_id'] = results.id
        messages.add_message(request, messages.SUCCESS, 'Welcome back, {}'.format(results))
        return redirect('/dashboard')
    else:
        for key in results:
            messages.add_message(request, messages.ERROR, results[key])
    return redirect("/")
def dashboard(request):
    context = {
        "products":Product.objects.all()
    }
    return render(request, 'dashboard.html', context)
def logout(request):
    request.session.clear()
    return redirect('/')
def home(request):
    return redirect('/dashboard')
def newitem(request):
    return redirect('/new')
def new(request):

    return render(request, "newitem.html")
def products(request):
    added_products = User.objects.get(id=request.session["User_id"]).added_products.all()
    products = Product.objects.all()
    for product in added_products:
        products = products.exclude(id=product.id)
    return render(request, "dashboard.html", {"products": products, "added_products": added_products})
def addproduct(request):
    results = Product.objects.addproduct(request.POST, request.session['User_id'])
    print(results)
    if isinstance(results, Product):
        messages.add_message(request, messages.SUCCESS, 'You successfully added an item!')
        product = Product.objects.get(id=results.id)
        user = User.objects.get(id=request.session['User_id'])
        product.added.add(user)
        return redirect('/products')
    else:
        for key in results:
            messages.add_message(request, messages.ERROR, results[key])
    return redirect('/new')
def addpro(request, product_id):
    product = Product.objects.get(id=product_id)
    user = User.objects.get(id=request.session['User_id'])
    product.added.add(user)
    return redirect("/products")
def removepro(request, product_id):
    product = Product.objects.get(id=product_id)
    user = User.objects.get(id=request.session['User_id'])
    product.added.remove(user)
    return redirect("/products")
def info(request, product_id):
    product = Product.objects.get(id=product_id)
    context = {
        "product":product
    }
    return render(request, "info.html",context)



