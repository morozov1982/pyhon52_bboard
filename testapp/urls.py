from django.urls import path

from bboard.views import index
from testapp.views import add_img

app_name = 'testapp'

urlpatterns = [
    path('add/', add_img, name='add'),
    path('', index, name='index'),
]
