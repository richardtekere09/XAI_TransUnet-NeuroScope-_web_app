from django.urls import path
from django.urls import path
from .views import home, signup_view, login_view, logout_view, profile_view,  change_password  # Import functions directly
from django.urls import path, include

urlpatterns = [
    path('', home, name='home'),
    path('signup/', signup_view, name='signup'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('profile/', profile_view, name='profile'),
    path('change_password/', change_password, name='change_password'),
    path('auth/', include('social_django.urls', namespace='social')),
]

