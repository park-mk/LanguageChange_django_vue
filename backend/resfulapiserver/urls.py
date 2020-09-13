from django.conf.urls import url, include
from Users import views
from django.urls import path



urlpatterns = [

    url('api/send_user_status/', views.send_user_status),
    url('api/update_user_status/', views.update_user_status),
    url('api/userslist/', views.super_user_list),
    #url('api/usersapplylist/', views.super_view_rent_user),
    url('api/statusup/', views.super_update_user),
    url('api/user_apply_status_up',views.user_apply_status_up),
    url('api/statusdown/', views.super_downdate_user),
    url('api/user_rent_apply/',views.user_rent_apply),
    url('api/deny_apply_a/', views.super_deny_apply),
    url('api/history_to_user',views.history_to_user),
    path('api/delete/', views.super_del_user),
    path('api/render',views.user_get_your_status),
    path('api/allow_return/', views.allow_return),
    path('api/apply_userinfo/', views.super_view_rent_user_info),

    path('api/data_ana/', views.data_ana),
    url('api/login/', views.login),
    url('api/register/',views.register_mail_post),
    url(r'^activate/(?P<token>\w+.[-_\w]*\w+.[-_\w]*\w+)/$', views.user_verified, name='activate'),
    url('api/equip/', include('Equipment.urls')),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),



]

