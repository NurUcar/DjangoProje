from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from home.models import Setting
from order.models import ShopCartForm, ShopCart
from product.models import Category


def index(request):
    return HttpResponse("Order App")


@login_required(login_url='login')
def addtocart(request, id):
    url = request.META.get('HTTP_REFERER')
    current_user = request.user
    checkproduct = ShopCart.objects.filter(product_id=id)
    if checkproduct:
        control = 1
    else:
        control = 0
    if request.method == 'POST':
        form = ShopCartForm(request.POST)
        if form.is_valid():
            if control == 1:
                data = ShopCart.objects.get(product_id=id)
                data.quantity += form.cleaned_data['quantity']
                data.save()
            else:
                data = ShopCart()
                data.user_id = current_user.id
                data.product_id = id
                data.quantity = form.cleaned_data['quantity']
                data.save()
            request.session['cart_items']= ShopCart.objects.filter(user_id=current_user.id).count()
            messages.success(request, "Ürün başarı ile sepete eklenmiştir. Teşekkür Ederiz.")
            return HttpResponseRedirect(url)

    else:
        if control == 1:
            data = ShopCart.objects.get(product_id=id)
            data.quantity += 1
            data.save()
        else:
            data = ShopCart()
            data.user_id = current_user.id
            data.product_id = id
            data.quantity = 1
            data.save()
        request.session['cart_items'] = ShopCart.objects.filter(user_id=current_user.id).count()
        messages.success(request, "Ürün başarı ile sepete eklenmiştir. Teşekkür Ederiz.")
        return HttpResponseRedirect(url)
    messages.warning(request, "Ürün sepete eklenemedi!. Lütfen kontrol ediniz..")
    return HttpResponseRedirect(url)


@login_required(login_url='/login')
def shopcart(request):
    category = Category.objects.all()
    setting = Setting.objects.get(pk=1)
    current_user = request.user
    shop_cart = ShopCart.objects.filter(user_id=current_user.id)
    request.session['cart_items'] = ShopCart.objects.filter(user_id=current_user.id).count()

    total = 0
    for rs in shop_cart:
        total += rs.product.price * rs.quantity
    context = {'shop_cart': shop_cart,
               'category': category,
               'total': total,
               'setting': setting,
               }
    return render(request, 'Shopcart_products.html', context)


@login_required(login_url='/login')
def deletefromcart(request, id):
    ShopCart.objects.filter(id=id).delete()
    current_user=request.user
    request.session['cart_items'] = ShopCart.objects.filter(user_id=current_user.id).count()
    messages.success(request, "Ürün başarılı bir şekilde sepetten kaldırılmıştır.")
    return HttpResponseRedirect("/shopcart")
