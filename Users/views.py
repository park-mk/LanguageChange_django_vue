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
def register_mail_post(request):

    if request.method == 'POST':
        #当在 api／register中有post 请求 输入{username: password: email :}d的时候 向指定的email发送认证email 并保证该email 可以重新
        #跑动 新的函数 def user_verified
        return HttpResponse({'data':'success'}, status=200)


    return HttpResponse({'data':'fail'}, status=200)



@csrf_exempt
def user_verified(request):
    #当用户在自己的邮箱点击 认证token时会启动该函数 并将该user的 is_verified转换为 true
    return HttpResponse({'data': 'succes'}, status=200)
