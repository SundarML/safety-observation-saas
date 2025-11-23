# observations/urls.py
from django.urls import path
from . import views

app_name = 'observations'

urlpatterns = [
    path('', views.observation_list, name='observation_list'),
    path('new/', views.ObservationCreateView.as_view(), name='create'),
    path('<int:pk>/', views.ObservationDetailView.as_view(), name='detail'),
    path('<int:pk>/rectify/', views.RectificationUpdateView.as_view(), name='rectify'),
    path('<int:pk>/verify/', views.VerificationView.as_view(), name='verify'),

    # Export URLs
    path('export/csv/', views.export_observations_csv, name='export_observations_csv'),
    path('export/excel/', views.export_observations_excel, name='export_observations_excel'),
]

