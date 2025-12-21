from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import Index, SignupView, CustomLoginView, WorkListView, WorkDetailView, WorkCreateView

urlpatterns = [
    path('', Index.as_view(), name='index'),
    path('signup/', SignupView.as_view(), name='signup'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='index'), name='logout'),
    
    # Work URLs
    path('works/', WorkListView.as_view(), name='work_list'),
    path('works/create/', WorkCreateView.as_view(), name='work_create'),
    path('works/<int:pk>/', WorkDetailView.as_view(), name='work_detail'),
]
