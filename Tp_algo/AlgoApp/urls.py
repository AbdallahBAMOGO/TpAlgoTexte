from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('compare/', views.compare_documents, name='compare_documents'),
]