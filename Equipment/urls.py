from django.conf.urls import url, include
from . import views
from django.urls import path

urlpatterns = [
    path('update/<str:id>', views.provider_update_equip),
    path('on/<str:id>',views.provider_on_equip),
    path('off/<str:id>', views.provider_off_equip),
    path('equip/<int:id>/', views.equip),
    path('deny/', views.deny_equip),
    path('rentlist/', views.equip_rent_list),
    path('rentlist/<str:id>', views.equip_rent_list_specific),
    path('rentdescription/',views.equip_borrow_user_info),
    path('accept_rent_apply/',views.accept_rent_equip),
    path('accept_rent_deny/',views.deny_rent_equip),
    path('delete／', views.provider_del_equip),
    path('equiplist/',views.equip_list),
    path('equiponlist/',views.equip_on_list),
    path('description/',views.super_view_apply_equip_info)


]