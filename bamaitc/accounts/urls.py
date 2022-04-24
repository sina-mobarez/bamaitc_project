from django.urls import path, include
from .views import LoginView, VerifyView, ResendVerifyView, RegisterView, invite_code


urlpatterns = [
        
        path('login/', LoginView.as_view(), name='login-not-auth'),
        path('verify-phone-number/', VerifyView.as_view(), name='verify'),
        path('verify-phone-number/resend/', ResendVerifyView.as_view(), name='resend'),
        path('register/', RegisterView.as_view(), name='register-not-auth'),
        path('invite-code/', invite_code, name='invite-code'),
        path('acoounts/', include('django.contrib.auth.urls')),
]