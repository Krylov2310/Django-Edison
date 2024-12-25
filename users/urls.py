from django.urls import path
from .views import home, profile, RegisterView, user_logout

urlpatterns = [
    path('', home, name='users-home'),
    path('register/', RegisterView.as_view(), name='users-register'),
    path('profile/', profile, name='users-profile'),
    path('logout/', user_logout, name='logout'),
]
