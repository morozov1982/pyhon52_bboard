from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.db import transaction
from django.db.transaction import atomic
from django.shortcuts import render, redirect

from testapp.forms import ImgForm
from testapp.models import Img


# @transaction.non_atomic_requests
# @transaction.atomic
# def my_view(request):
#     if formset.is_valid():
#         with atomic():
#             pass


def add_img(request):
    if request.method == 'POST':
        form = ImgForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('testapp:add')
    else:
        form = ImgForm()

    imgs = Img.objects.all()

    context = {'form': form, 'imgs': imgs}
    return render(request, 'testapp/add.html', context)


# user1 = User.objects.create_user('ivanov', password='1234567890',
#                                  email='ivanov@site.kz')
# user2 = User.objects.create_user('petrov', password='0987654321',
#                                  email='petrov@site.kz')
#
# admin2 = User.objects.create_superuser('sidorov', password='7777777',
#                                  email='sidorov@site.kz')
#
# admin = User.objects.get(name='admin')
# if admin.check_password('password'):
#     pass  # пароли совпадают
# else:
#     pass  # пароли НЕ совпадают
#
# admin.set_password('newpassword')
# admin.save()
#
# def my_login(request):
#     username = request.POST['username']
#     password = request.POST['password']
#     user = authenticate(request, username=username, password=password)
#     if user is not None:
#         login(request, user)
#         # вход выполнен
#     else:
#         pass  # вход не выполнен
#
# def my_logout(request):
#     logout(request)
#     # Перенаправить на какую-нибудь страницу
