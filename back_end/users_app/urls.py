from django.urls import path
from . import views

urlpatterns = [
    path('sign_in/', views.sign_in, name='sign_in'),
    path('sign_up/', views.sign_up, name='sign_up'),
    path('sign_out/', views.sign_out, name='sign_out'),
    path('ft_api/', views.ft_api, name="ft_api"),
    path('check_authorize/', views.check_authorize, name="check_authorize"),
    path('profile/', views.profile, name="profile"),
]