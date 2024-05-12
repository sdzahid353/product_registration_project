from django.urls import path
from .views import RegisterUserView, LoginView

urlpatterns = [
    path('register/', RegisterUserView.as_view(), name='user-register'),
    path('login/', LoginView.as_view(), name='user-login'),
]
