from django.urls import path
from likes import views


urlpatterns = [
    path('like_change', views.like_change, name='like_change'),
    path('par_change',views.par_change, name='par_change'),
]