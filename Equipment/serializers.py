from rest_framework import serializers
from .models import Equip


class EquipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Equip
        fields = '__all__'

#or fields =['name','is_active'] if you want specific value

