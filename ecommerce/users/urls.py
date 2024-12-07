from django.urls import path
from . import views
from shop import views as shop_views
from django.contrib.auth.views import PasswordChangeView
from shop.views import add_good
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),
    path('profile/password/', PasswordChangeView.as_view(), name='password_change'),
    path('add/', shop_views.add_good, name='add_good'),
    path('edit/<int:good_id>/', shop_views.edit_good, name='edit_good'),
    path('delete/<int:good_id>/', shop_views.delete_good, name='delete_good'),
    path('goods/<int:pk>/', shop_views.good_detail, name='good_detail')
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


