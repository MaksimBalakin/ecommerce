from django.urls import path
from . import views
from django.contrib.auth.views import PasswordChangeView

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),
    path('profile/password/', PasswordChangeView.as_view(), name='password_change'),
]

