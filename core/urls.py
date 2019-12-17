from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', views.index, name="index"),
    path('home', views.home, name="home"),
    path('login', views.login, name="login"),
    path('logout', auth_views.LogoutView.as_view(), name="logout"),
    path('change', auth_views.PasswordResetView.as_view()),
    path('signup', views.signup, name="signup"),
    path('crawling', views.crawling, name='crawling'),
]