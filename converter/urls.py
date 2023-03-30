from django.urls import path
from .views import index, register, user_login, user_logout

urlpatterns = [
    path('', index),
    path('logout/', user_logout, name='logout'),
    path('register/', register, name='register'),
    path('login/', user_login, name='login'),

]