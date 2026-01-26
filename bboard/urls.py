from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from bboard.views import (index,
                          BbCreateView, BbRubricBbsView,
                          BbDetailView, BbUpdateView, BbDeleteView, rubrics, bbs)

app_name = 'bboard'

urlpatterns = [
    path('add/', BbCreateView.as_view(), name='add'),

    path('rubrics/', rubrics, name='rubrics'),
    path('bbs/<int:rubric_id>/', bbs, name='bbs'),

    path('update/<int:pk>/', BbUpdateView.as_view(), name='update'),
    path('delete/<int:pk>/', BbDeleteView.as_view(), name='delete'),
    path('<int:rubric_id>/', BbRubricBbsView.as_view(), name='by_rubric'),
    path('detail/<int:pk>/', BbDetailView.as_view(), name='detail'),

    path('accounts/login/', LoginView.as_view(), name='login'),
    path('accounts/logout/', LogoutView.as_view(next_page='bboard:index'), name='logout'),

    path('', index, name='index'),
]
