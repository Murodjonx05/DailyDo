from django.urls import path
from .views import Index
from .account_views import LoginView, SignUpView, logout_view
urlpatterns = [
    path('', Index.as_view(), name='index'),
    path('accounts/login/', LoginView.as_view(), name='login'),
    path('accounts/signup/', SignUpView.as_view(), name='signup'),
    path('accounts/logout/', logout_view, name='logout'),
]
