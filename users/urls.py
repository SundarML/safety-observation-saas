# users/urls.py
from django.urls import path, include
from .views import register, profile_view
from .views import CustomLoginView
from django.contrib.auth import views as auth_views
from users.forms import EmailLoginForm


app_name = 'users'

urlpatterns = [
    path('profile/', profile_view, name='profile'),
    path("accounts/login/", auth_views.LoginView.as_view(
        template_name="users/login.html",
        authentication_form=EmailLoginForm
    ), name="login"),
    # path('login/', CustomLoginView.as_view(), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    # path('', include('observations.urls')),
    path('register/', register, name='register'),

]
