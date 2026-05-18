from django.urls import path
from . import views

urlpatterns = [

    path('', views.login_page),

    path('register/', views.register_page),

    path('verify-otp/', views.verify_otp),

    path('dashboard/', views.dashboard),

    path('logout/', views.logout_page),

]