from django.conf.urls import url, include
from . import views
from django.urls import path

urlpatterns = [
    path('update/<str:id>', views.provider_update_equip),
    path('on/<str:id>',views.provider_on_equip),
    path('off/<str:id>', views.provider_off_equip),
    path('delete/<str:id>', views.provider_del_equip),
    path('equiplist/',views.equip_list)


]