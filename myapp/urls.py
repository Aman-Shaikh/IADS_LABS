from django.urls import path
from . import views

app_name = 'myapp'  # Define the namespace

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('<int:book_id>/', views.detail, name='detail'),
    path('orders/', views.orders, name='orders'),
    path('feedback/', views.getFeedback, name='feedback'),
    path('orderform/', views.orderformlab, name='feedback'),
    path('place_order/', views.place_order, name='place_order'),
    path('findbooks/', views.findbooks, name='findbooks'),
    path('review/', views.review, name='review'),
]
