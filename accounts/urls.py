from django.urls import path
from . import views


app_name = 'accounts'
urlpatterns = [
    path('login/', views.login, name='login'),
    path('login_for_medal', views.login_for_medal, name='login_for_medal'),
    path('login_test/',views.login_test, name='login_test'),
    path('logout/', views.logout, name='logout'),
    path('register/',views.register,name='register'),
    path('confirm/<str:code>/', views.confirm, name='confirm'),
    path('cover_page/', views.index, name='cover_page'),
    path('userinfo/', views.userinfo, name='userinfo'),
    path('pswchange/', views.pswchange_request, name='pswchange_request'),
    path('pswchange/<str:code>/', views.pswchange, name='pswchange'),
    path('pswforget/', views.pswforget, name='pswforget'),
]