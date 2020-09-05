from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Users
from .serializers import UsersSerializer
from rest_framework.parsers import JSONParser
from django.contrib.auth.models import User
from rest_framework import generics, status

from django.contrib.auth import authenticate
import json
from rest_framework.authtoken.models import Token


# Create your views here.
@csrf_exempt
def user_list(request):
    if request.method == 'GET':
        query_set = Users.objects.all()
        serializer = UsersSerializer(query_set, many=True)
        print("get!!!! mota!")
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        print("post!!")
        print(request)
        data = JSONParser().parse(request)
        serializer = UsersSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)


@csrf_exempt
def user(request, pk):

    obj = Users.objects.get(pk=pk)
    print(obj)
    if request.method == 'GET':
        serializer = UsersSerializer(obj)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = UsersSerializer(obj, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        obj.delete()
        return HttpResponse(status=204)



@csrf_exempt





def login(request):

    if request.method == 'POST':
        print('to here')
        data = JSONParser().parse(request)
        search_name = data['name']
        print('to here')
        obj = Users.objects.get(name=search_name)
        data = JSONParser().parse(request)
        search_name = data['name']
        obj = Users.objects.get(name=search_name)

        if data['phone_number'] == obj.phone_number :
            print("login!!!")
            return HttpResponse(status=200)
        else:
            print("fail!!")
            return HttpResponse(status=401)


    return render(request, 'Users/login.html')



@csrf_exempt
def chat_service(request):
    if request.method == 'POST':
        input1 = request.POST['input1']
        print(input1)
        output = dict()
        output['response'] = "this is reply"
        return HttpResponse(json.dumps(output), status=200)
    else:
        return render(request, 'Users/chat_t:wqest.html')