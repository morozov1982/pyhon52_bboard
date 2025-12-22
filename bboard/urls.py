from django.urls import path

from bboard.views import (index,
                          BbCreateView, BbRubricBbsView,
                          BbDetailView, BbUpdateView, BbDeleteView)

app_name = 'bboard'

urlpatterns = [
    path('add/', BbCreateView.as_view(), name='add'),
    path('update/<int:pk>/', BbUpdateView.as_view(), name='update'),
    path('delete/<int:pk>/', BbDeleteView.as_view(), name='delete'),
    path('<int:rubric_id>/', BbRubricBbsView.as_view(), name='by_rubric'),
    path('detail/<int:pk>/', BbDetailView.as_view(), name='detail'),
    path('', index, name='index'),
]
