from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('stations', views.stations, name='stations'),
    path('signup', views.signup, name='signup'),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path('send-password-reset', views.send_password_reset, name='send_password_reset'),
    path('reset-password', views.reset_password, name='reset_password'),
    path('profile', views.profile, name='profile'),
    path('admin', views.admin, name='admin'),
    path('search', views.search, name='search'),
    path('seats', views.seats, name='seats'),
    path('orders', views.orders, name='orders'),
    path('payment-completed', views.payment_completed, name='payment_completed'),
    path('verify', views.verify, name='verify'),
    path('qrcode', views.create_qrcode, name='create_qrcode'),
    path('confirm', views.confirm_account, name='confirm_account'),
]

handler404 = views.handle_404
handler500 = views.handle_500
