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
