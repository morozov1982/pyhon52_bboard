from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.db import transaction
from django.db.transaction import atomic
from django.shortcuts import render, redirect
from django.template.loader import render_to_string

from testapp.forms import ImgForm
from testapp.models import Img


def add_img(request):
    if request.session.test_cookie_worked():
        request.session.delete_test_cookie()
        print('COOKIES удалены!!!')
    else:
        print('Просим клиента включить COOKIES')

    request.session.set_test_cookie()

    # if 'counter' in request.COOKIES:
    if 'counter' in request.session:
        # cnt = int(request.COOKIES['counter']) + 1
        cnt = request.session['counter'] + 1
    else:
        cnt = 1

    if request.method == 'POST':
        form = ImgForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('testapp:add')
    else:
        form = ImgForm()

    imgs = Img.objects.all()

    context = {'form': form, 'imgs': imgs, 'counter': cnt}

    request.session['counter'] = cnt
    response = HttpResponse(render_to_string('testapp/add.html', context, request))
    response.set_cookie('counter', cnt)

    if cnt >= 10:
        response.delete_cookie('counter')

    return response
    # return render(request, 'testapp/add.html', context)
