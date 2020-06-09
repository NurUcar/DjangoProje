from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect

from product.models import CommentFrom, Comment


# Create your views here.
def index(request):
    return render("Product page")


@login_required(login_url='/login')  # check login
def addcomment(request, id):
    url = request.META.get('HTTP_REFERER')
    if request.method == 'POST':
        form = CommentFrom(request.POST)
        if form.is_valid():
            current_user = request.user  # Access User session info
            data = Comment()
            data.user_id = current_user.id
            data.product_id = id
            data.subject = form.cleaned_data['subject']
            data.comment = form.cleaned_data['comment']
            data.rate = form.cleaned_data['rate']
            data.ip = request.META.get('REMOTE_ADDR')
            data.save()
            messages.success(request, "Yorumunuz başarı ile gönderilmiştir. Teşekkür Ederiz..")
            return HttpResponseRedirect('/')
        messages.warning("Yorumunuz Gönderilemedi. Lütfen kontrol ediniz..")
    return HttpResponseRedirect(url)
