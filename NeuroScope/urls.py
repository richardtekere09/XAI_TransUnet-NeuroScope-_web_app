from django.urls import path, include
from . import views
from .views import home, signup_view, login_view, logout_view, profile_view,  change_password , neurocheck_view, blog_view # Import functions directly

urlpatterns = [
    path('neurocheck/', neurocheck_view, name='neurocheck'),
    path('blog/', blog_view, name='blog'),
    path('', home, name='home'),
    path('signup/', signup_view, name='signup'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('profile/', profile_view, name='profile'),
    path('change_password/', change_password, name='change_password'),
    path('auth/', include('social_django.urls', namespace='social')),
    path('neurocheck_chat/', views.neurocheck_chat, name='neurocheck_chat'),
    path('upload/', views.upload_mri, name='upload_mri'),
]

