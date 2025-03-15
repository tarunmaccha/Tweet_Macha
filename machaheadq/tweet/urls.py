from django.urls import path
from django.contrib.auth.views import LoginView
from . import views 

urlpatterns = [
    path('login/', LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('', views.tweet_list, name='tweet_list'),
    path('create/',views.tweet_create, name='tweet_create'),
    path('<int:tweet_id>/edit/',views.tweet_edit, name='tweet_edit'),
    path('<int:tweet_id>/delete/',views.tweet_delete, name='tweet_delete'),
    path('register/', views.register, name='register'),
    path('search/', views.tweet_search, name='tweet_search'),
]