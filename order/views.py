from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from home.models import Setting, UserProfile
from order.models import ShopCartForm, ShopCart, OrderForm, Order, OrderProduct
from product.models import Category, Product
from django.utils.crypto import get_random_string


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
            request.session['cart_items'] = ShopCart.objects.filter(user_id=current_user.id).count()
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
    current_user = request.user
    request.session['cart_items'] = ShopCart.objects.filter(user_id=current_user.id).count()
    messages.success(request, "Ürün başarılı bir şekilde sepetten kaldırılmıştır.")
    return HttpResponseRedirect("/shopcart")


@login_required(login_url='/login')
def orderproduct(request):
    category = Category.objects.all()
    setting = Setting.objects.get(pk=1)
    current_user = request.user
    shop_cart = ShopCart.objects.filter(user_id=current_user.id)
    total = 0
    for rs in shop_cart:
        total += rs.product.price * rs.quantity

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            data = Order()
            data.first_name = form.cleaned_data['first_name']
            data.last_name = form.cleaned_data['last_name']
            data.address = form.cleaned_data['address']
            data.city = form.cleaned_data['city']
            data.phone = form.cleaned_data['phone']
            data.user_id = current_user.id
            data.total = total
            data.ip = request.META.get('REMOTE_ADDR')
            ordercode = get_random_string(5).upper()
            data.code = ordercode
            data.save()

            shop_cart = ShopCart.objects.filter(user_id=current_user.id)
            for rs in shop_cart:
                detail = OrderProduct()
                detail.order_id = data.id
                detail.product_id = rs.product_id
                detail.user_id = current_user.id
                detail.quantity = rs.quantity
                product = Product.objects.get(id=rs.product_id)
                product.amount -= rs.quantity
                product.save()
                detail.price = rs.product.price
                detail.amount = rs.amount
                detail.save()
            ShopCart.objects.filter(user_id=current_user.id).delete()
            request.session['cart_items'] = 0
            messages.success(request, "Siparisiniz tamamlanmıştır. Tesekkürler..")
            return render(request, 'Order_Completed.html', {'ordercode': ordercode, 'category': category})
        else:
            messages.warning(request, form.errors)
            return HttpResponseRedirect("/order/orderproduct")
    form = OrderForm()
    profile = UserProfile.objects.get(user_id=current_user.id)
    context = {
        'setting': setting,
        'shop_cart': shop_cart,
        'category': category,
        'total': total,
        'form': form,
        'profile': profile,
    }
    return render(request, 'Order_Form.html', context)
