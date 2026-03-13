from django.core.mail import EmailMessage, get_connection, EmailMultiAlternatives, send_mail, send_mass_mail

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


# Низкоуровневые инструменты
# def test_email(request):
#     # em = EmailMessage(
#     #     subject='Test',
#     #     body='Test',
#     #     to=['user@supersite.kz']
#     # )
#     # em.send()
#
#     # em = EmailMessage(
#     #     subject='Ваш новый пароль',
#     #     body='Ваш новый пароль находится во вложении',
#     #     attachments=[('password.txt', '123456789', 'text/plain')],
#     #     to=['user@supersite.kz']
#     # )
#     # em.send()
#
#     # em = EmailMessage(
#     #     subject='Ваш новый пароль',
#     #     body='Ваш новый пароль находится во вложении',
#     #     to=['user@supersite.kz']
#     # )
#     # em.attach_file(r'./requirements.txt')
#     # em.send()
#
#     ### На основе шаблонов ###
#     # context = {'user': 'Вася Пупкин'}
#     # s = render_to_string('email/letter.txt', context)
#     # em = EmailMessage(
#     #     subject='Оповещение',
#     #     body=s,
#     #     to=['vpupkin@othersite.kz']
#     # )
#     # em.send()
#
#     ### Использование соединений ###
#     # con = get_connection()
#     # con.open()
#     # email1 = EmailMessage(..., connection=con)
#     # email1.send()
#     # email2 = EmailMessage(..., connection=con)
#     # email2.send()
#     # email3 = EmailMessage(..., connection=con)
#     # email3.send()
#     # con.close()
#
#     # con = get_connection()
#     # con.open()
#     # email1 = EmailMessage(...)
#     # email2 = EmailMessage(...)
#     # email3 = EmailMessage(...)
#     # con.send_messages([email1, email2, email3])
#     # con.close()
#
#     ### Составное письмо ###
#     em = EmailMultiAlternatives(
#         subject='Test',
#         body='Test',
#         to=['user@supersite.kz']
#     )
#     em.attach_alternative('<h1>Test</h1>', 'text/html')
#     em.send()
#
#     return HttpResponse("Тестим мыло")


# Высокоуровневые инструменты
def test_email(request):
    # send_mail(
    #     'Test mail',
    #     'Test!!!',
    #     'webmaster@supersite.kz',
    #     ['user@othersite.kz'],
    #     html_message='<h1>Test!!!</h1>'
    # )

    msg1 = ('Подписка', 'Подтвердите подписку', 'subscribe@supersite.kz',
            ['user@othersite.kz', 'user2@othersite.kz'])
    msg2 = ('Подписка', 'Подписка подтверждена', 'subscribe@supersite.kz',
            ['megauser@megasite.kz'])
    send_mass_mail((msg1, msg2))

    return HttpResponse("Тестим мыло")
