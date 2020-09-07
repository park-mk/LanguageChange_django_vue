from django.conf.urls import url, include
from . import views


urlpatterns = [
      url('add', views.equip_list),
      url('wa',views.equip),
  ]