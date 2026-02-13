from django.urls import path
from .views import request_demo_view, organization_signup
from . import views
app_name = "core"
urlpatterns = [
    path("request-demo/", request_demo_view, name="request_demo"),
    path("signup/", organization_signup, name="organization_signup"),
    path("invite/", views.invite_user, name="invite_user"),
    path("accept-invite/<uuid:token>/", views.accept_invite, name="accept_invite"),
]
