from django.urls import path

from bboard.views import index
from testapp.views import add_img, test_email

app_name = 'testapp'

urlpatterns = [
    path('add/', add_img, name='add'),
    path('test_email/', test_email, name='test_email'),
    path('', index, name='index'),
]
