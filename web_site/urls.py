from django.urls import path


from . import views

app_name = 'web_site'
urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('login_user/', views.login_user, name='login_user'),
    path('logout_request/', views.logout_request, name='logout_request'),
    path('apply_request/', views.apply_request,  name='apply_request'),
    path('smjer/<pk>/', views.smjer, name='smjer'),
]