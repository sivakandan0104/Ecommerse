from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('members/', views.members, name='members'),
    path('register/', views.forms, name='forms'),
    path('login/', views.login, name='login'),
    path('forgotpass/', views.forgotpass, name='forgot'),
    path('logout/', views.logout, name='logout'),
    
    path('main/', views.main, name='main'),
    
    path('add-to-cart/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart, name='cart'),
    path('update-quantity/', views.update_quantity, name='update_quantity'),
    path('delete-product/', views.delete_product, name='delete_product'),

    path('purchase/', views.orderpay, name='purchase'),
    path('purchase/verify_payment/', views.verify_payment, name='verify_payment'),
    path('success/',views.success, name='success'),
    path('failure/',views.failure, name='failure'),
]
