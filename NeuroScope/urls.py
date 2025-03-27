from django.urls import path, include
from .views import home, signup_view, login_view, logout_view, profile_view,  change_password ,  public_home, neurocheck_view, blog_view # Import functions directly


urlpatterns = [
    path('', public_home, name='home1'),  # Make it default route
    path('neurocheck/', neurocheck_view, name='neurocheck'),
    path('blog/', blog_view, name='blog'),
    path('', home, name='home'),
    path('signup/', signup_view, name='signup'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('profile/', profile_view, name='profile'),
    path('change_password/', change_password, name='change_password'),
    path('auth/', include('social_django.urls', namespace='social')),
]

