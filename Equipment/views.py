from .models import Equip
from .serializers import EquipSerializer
from rest_framework.parsers import JSONParser
from django.http import HttpResponse, JsonResponse

# Create your views here.
def equip_list(request):
    if request.method == 'GET':
        query_set = Equip.objects.all()
        serializer = EquipSerializer(query_set, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = EquipSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)



def equip(request, pk):

    obj = Equip.objects.get(pk=pk)

    if request.method == 'GET':
        serializer = EquipSerializer(obj)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = EquipSerializer(obj, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        obj.delete()
        return HttpResponse(status=204)
