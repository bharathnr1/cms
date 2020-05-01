from django.urls import path

from . import views

app_name = 'accounts'

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('password_change/', views.change_password, name='change_password'),

    # Waiting for Admin's approval
    path('pending_approval/', views.pending_approval, name='pending_approval'),
]