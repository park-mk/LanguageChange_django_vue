from django.conf.urls import url, include
from . import views
from django.urls import path

urlpatterns = [
    path('update/<str:id>', views.provider_update_equip),
    path('delete/<str:id>', views.provider_del_equip),
    path('on/<str:id>', views.provider_del_equip),

]