from django.urls import path
from .views import AllUsersView, RegisterView, activate_user
from users import views


urlpatterns = [
    
path('users/activate/<str:token>/', views.activate_user, name='activate'),
path('users/', AllUsersView.as_view(), name='all_users'),
path('', views.home, name='home'),
path('register/', RegisterView.as_view(), name='register'),
]