from django.urls import path
from . import views

app_name = "accounts"
urlpatterns = [
    # if you are not logged in you get to the login page
    # if you are logged in you go to your profile this is a redirecting page
    # path('', auth_views.LoginView.as_view(template_name='login/login.html'),
    # name=''),
    path('profile/', views.show_profile, name='profile'),
]
