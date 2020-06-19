import json

from django.contrib import messages
from django.contrib.auth import logout, authenticate, login
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from home.forms import SearchForm, SignUpForm
from home.models import Setting, ContactForm, ContactFormMessage, UserProfile
from order.models import ShopCart
from product.models import Product, Category, Images, Comment


def index(request):
    current_user = request.user
    setting = Setting.objects.get(pk=1)
    sliderdata = Product.objects.all()[:4]
    category = Category.objects.all()
    dayproducts = Product.objects.all()[:4]
    lastproducts = Product.objects.all().order_by('-id')[:4]
    randomproducts = Product.objects.all().order_by('?')[:4]
    request.session['cart_items'] = ShopCart.objects.filter(user_id=current_user.id).count()
    total = 0
    shop_cart = ShopCart.objects.filter(user_id=current_user.id)
    for rs in shop_cart:
        total += rs.product.price * rs.quantity
    context = {'setting': setting,
               'category': category,
               'page': 'home',
               'total': total,
               'sliderdata': sliderdata,
               'dayproducts': dayproducts,
               'lastproducts': lastproducts,
               'randomproducts': randomproducts, }
    return render(request, 'index.html', context)


def aboutus(request):
    setting = Setting.objects.get(pk=1)
    category = Category.objects.all()
    total = 0
    current_user = request.user
    shop_cart = ShopCart.objects.filter(user_id=current_user.id)
    for rs in shop_cart:
        total += rs.product.price * rs.quantity
    context = {'setting': setting,
               'page': 'aboutus',
               'total': total,
               'category': category, }
    return render(request, 'aboutus.html', context)


def references(request):
    setting = Setting.objects.get(pk=1)
    category = Category.objects.all()
    current_user = request.user
    shop_cart = ShopCart.objects.filter(user_id=current_user.id)
    total = 0
    for rs in shop_cart:
        total += rs.product.price * rs.quantity
    context = {'setting': setting,
               'page': 'references',
               'total': total,
               'category': category, }
    return render(request, 'references.html', context)


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)

        if form.is_valid():
            data = ContactFormMessage()
            data.name = form.cleaned_data['name']
            data.email = form.cleaned_data['email']
            data.subject = form.cleaned_data['subject']
            data.message = form.cleaned_data['message']
            data.ip = request.META.get('REMOTE_ADDR')
            data.save()
            messages.success(request, "Mesajınız başarı ile gönderilmiştir. Teşekkür ederiz.")
            return HttpResponseRedirect('/contact')

    setting = Setting.objects.get(pk=1)
    category = Category.objects.all()
    current_user = request.user
    shop_cart = ShopCart.objects.filter(user_id=current_user.id)
    total = 0
    for rs in shop_cart:
        total += rs.product.price * rs.quantity
    form = ContactForm()
    context = {'setting': setting,
               'form': form,
               'category': category,
               'total': total, }
    return render(request, 'contact.html', context)


def category_products(request, id, slug):
    category = Category.objects.all()
    categorydata = Category.objects.get(pk=id)
    productCount = Product.objects.filter(category_id=id).count()
    products = Product.objects.filter(category_id=id)
    setting = Setting.objects.get(pk=1)
    current_user = request.user
    shop_cart = ShopCart.objects.filter(user_id=current_user.id)
    total = 0
    for rs in shop_cart:
        total += rs.product.price * rs.quantity
    context = {'products': products,
               'category': category,
               'categorydata': categorydata,
               'productCount': productCount,
               'total': total,
               'setting': setting,
               }
    return render(request, 'product.html', context)


def product_detail(request, id, slug):
    category = Category.objects.all()
    product = Product.objects.get(pk=id)
    setting = Setting.objects.get(pk=1)
    images = Images.objects.filter(product_id=id)
    comments = Comment.objects.filter(product_id=id, status='True')
    current_user = request.user
    shop_cart = ShopCart.objects.filter(user_id=current_user.id)
    total = 0
    for rs in shop_cart:
        total += rs.product.price * rs.quantity
    context = {'category': category,
               'product': product,
               'setting': setting,
               'images': images,
               'total': total,
               'comments': comments, }
    return render(request, 'product_detail.html', context)


def product_comment(request, id, slug):
    category = Category.objects.all()
    product = Product.objects.get(pk=id)
    setting = Setting.objects.get(pk=1)
    images = Images.objects.filter(product_id=id)
    current_user = request.user
    shop_cart = ShopCart.objects.filter(user_id=current_user.id)
    total = 0
    for rs in shop_cart:
        total += rs.product.price * rs.quantity
    context = {'category': category,
               'product': product,
               'setting': setting,
               'images': images,
               'total': total,
               }
    return render(request, 'product_comment.html', context)


def product_search(request):
    if request.method == 'POST':  # form post edildiyse
        form = SearchForm(request.POST)
        if form.is_valid():
            category = Category.objects.all()
            query = form.cleaned_data['query']
            product = Product.objects.filter(title__icontains=query)
            context = {
                'products': product,
                'category': category,
            }
            return render(request, 'product_search.html', context)
        return HttpResponseRedirect('/')


def product_search_auto(request):
    if request.is_ajax():
        q = request.GET.get('term', '')
        product = Product.objects.filter(title__icontains=q)
        results = []
        for rs in product:
            product_json = {}
            product_json = rs.title
            results.append(product_json)
        data = json.dumps(results)
    else:
        data = 'fail'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)


def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/')


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect('/')
        else:
            messages.warning(request, "Kullanıcı Adınız yada Sifreniz Yanlış!")
            return HttpResponseRedirect('/login')

    category = Category.objects.all()
    setting = Setting.objects.get(pk=1)
    context = {
        'category': category,
        'setting': setting,
    }
    return render(request, 'login.html', context)


def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            # create data in profile table for user
            current_user = request.user
            data = UserProfile()
            data.user_id = current_user.id
            data.image = "images/users/user.png"
            data.save()
            messages.success(request, "Hoşgeldiniz.. Sitemize başarılı bir şekilde üye oldunuz..")
            return HttpResponseRedirect('/')
        messages.warning(request, "Hata.. Lütfen kontrol ediniz..")
    form = SignUpForm()
    category = Category.objects.all()
    setting = Setting.objects.get(pk=1)
    context = {
        'category': category,
        'setting': setting,
        'form': form,
    }
    return render(request, 'signup.html', context)
