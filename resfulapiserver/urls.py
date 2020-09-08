from django.conf.urls import url, include
from Users import views


urlpatterns = [
    url('api/users/<int:pk>/', views.user),
    url('api/users/', views.user_list),
    url('api/login/', views.login),
    url('api/register',views.register_mail_post),
    url(r'^activate/(?P<token>\w+.[-_\w]*\w+.[-_\w]*\w+)/$', views.user_verified, name='activate'),
    url('api/equip/', include('Equipment.urls')),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]

