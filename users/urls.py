# users/urls.py
from django.urls import path, include
from .views import register, profile_view
from .views import CustomLoginView
from django.contrib.auth import views as auth_views

app_name = 'users'

urlpatterns = [
    path('profile/', profile_view, name='profile'),
    # path('login/', CustomLoginView.as_view(), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    # path('', include('observations.urls')),
    path('register/', register, name='register'),

]
