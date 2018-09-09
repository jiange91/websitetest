from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'miunottingham'
urlpatterns = [
    path('', views.main_page, name='main_page'),
    path('groups/', views.groups, name='groups'),
    path('groups/<int:group_id>/group_activities', views.group_acts, name='group_acts'),
    path('group_activities/<int:act_id>', views.details, name='details'),
    path('new_group/<int:userid>/', views.new_group, name='new_group'),
    path('new_activity/<int:group_id>/', views.new_activity, name='new_activity'),
    path('edit_activity/<int:act_id>/', views.edit_activity, name='edit_activity'),
    path('groupconfirm/<str:code>/<int:user_id>/',views.groupconfirm, name='groupconfirm'),
    path('edit_activity/<int:act_id>/delete/', views.delete_act, name='del_activity'),
]