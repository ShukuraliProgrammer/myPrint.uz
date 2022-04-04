
from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.loginView, name='login'),
    path('logout/', views.logoutView, name='logout'),
    path('order_list/', views.order_list, name='order_list'),
    path('order/', views.orderView, name='order'),
    path('order/edit/',views.update_orderView, name='order-detail'),
    path('invoice/', views.listView, name='invoice'),

]
