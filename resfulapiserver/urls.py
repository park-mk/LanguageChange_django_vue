from django.conf.urls import url, include
from Users import views


urlpatterns = [
    url('users/<int:pk>/', views.user),
    url('users/', views.user_list),
    url('login/', views.login),
    url('equip/', include('Equipment.urls')),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]

