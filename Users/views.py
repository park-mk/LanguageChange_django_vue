from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Users
from .serializers import UsersSerializer
from rest_framework.parsers import JSONParser
from django.contrib.auth.hashers import make_password,check_password

from django.contrib.auth.models import User
from rest_framework import generics, status

from django.contrib.auth import authenticate
import json
from rest_framework.authtoken.models import Token

from django.core.mail import send_mail      # 发送邮件模块
from .utils import token_confirm
DOMAIN = 'http://127.0.0.1:8000'        # 网站运行域
INVITATION = '5GH4T'             # 管理员邀请码

# Create your views here.
@csrf_exempt
def super_user_list(request):
    if request.method == 'GET':
        query_set = Users.objects.all()
        serializer = UsersSerializer(query_set, many=True)
        print("get!!!! mota!")
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        print("post!!")
        print(request)
        data = JSONParser().parse(request)
        data['password']=make_password(data['password'])
        serializer = UsersSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

def super_del_user(request,id):
    if request.method == 'POST':
        data = JSONParser().parse(request)
        search_name = data['userid']
        try:
            obj = Users.objects.get(userid=id)
        except:
            return JsonResponse({'status':'false','message':"no such user"}, status=500)
            obj.delete()
            serializer = UsersSerializer(obj)
            return JsonResponse(serializer.data, status=200)
        else:
            print("fail!!")
            return JsonResponse({'status':'false','message':"wrong pass word"}, status=500)



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
        data = JSONParser().parse(request)
        search_name = data['userid']
        try:
            obj = Users.objects.get(userid=search_name)
        except:
            return JsonResponse({'status':'false','message':"no such user"}, status=500)

        print('??')

        if check_password(data['password'],obj.password):
            # if verified =false return haven't verified
            print("login!!!")
            serializer = UsersSerializer(obj)
            return JsonResponse(serializer.data, status=200)
        else:
            print("fail!!")
            return JsonResponse({'status':'false','message':"wrong pass word"}, status=500)


    return render(request, 'Users/login.html')

@csrf_exempt
def register_mail_post(request):

    if request.method == 'POST':
        #当在 api／register中有post 请求 输入{username: password: email :}d的时候 向指定的email发送认证email 并保证该email 可以重新
        #跑动 新的函数 def user_verified

        # invitation: 邀请码 只有有正确邀请码的注册用户才可以成为管理员
        # is_provider: 是否注册成为提供者(可提供打勾选项)

        # 获取用户注册数据
        username = request.POST.get('username').strip()
        password = request.POST.get('password').strip()
        email = request.POST.get('email').strip()
        invitation = request.POST.get('invitation').strip()
        is_provider = request.POST.get('is_provider')

        # 验证是否注册过
        is_username_repeated = Users.objects.filter(username=username)
        is_email_repeated = Users.objects.filter(email=email)
        if is_username_repeated:
            return HttpResponse('该用户名已经被注册过，请重新注册', status=200)
        if is_email_repeated:
            return HttpResponse('该邮件已经被注册过，请重新注册', status=200)

        # 验证是否注册管理员（邀请码的正确性）
        is_manager = False
        if invitation:
            if invitation == INVITATION:
                is_manager = True
            else:                # 如果填写了邀请码但不一致，返回错误
                return HttpResponse('邀请码错误', status=200)

        # 不能同时成为两个身份
        if is_manager and is_provider:
            return HttpResponse('不能同时成为管理员和设备提供者', status=200)

        # 确认注册信息有效后，插入数据
        if is_manager:
            user = Users.objects.create_superuser(username=username, password=password, email=email)
        elif is_provider:
            user = Users.objects.create_user(username=username, password=password, email=email, is_provider=True)
        else:
            user = Users.objects.create_user(username=username, password=password, email=email, is_provider=False)

        # 邮箱验证
        token = token_confirm.generate_validate_token(username)
        token_url = '/'.join([DOMAIN, 'activate', token])
        message = "\n".join([u'{0},欢迎加入XX'.format(username),
                             u'请访问该链接，完成用户验证:',
                             token_url])
        send_mail(u'注册用户验证信息', message, '1326742692@qq.com', [email], fail_silently=False)

        return HttpResponse({'data':'success'}, status=200)

    return HttpResponse({'data':'fail'}, status=200)



@csrf_exempt
def user_verified(request, token):
    #当用户在自己的邮箱点击 认证token时会启动该函数 并将该user的 is_verified转换为 true
    try:
        username = token_confirm.confirm_validate_token(token)
    except:       # 令牌过期
        username = token_confirm.remove_validate_token(token)
        users = Users.objects.filter(username=username)
        for user in users:
            user.delete()  # 删除注册用户
        return HttpResponse(
            u'对不起，验证链接已经过期，请重新<a href=\"' + DOMAIN + u'/register\">注册</a>',
            status=200
        )

    try:
        user = Users.objects.get(username=username)
    except Users.DoesNotExist:
        return HttpResponse(u"对不起，您所验证的用户不存在，请重新注册", status=200)
    user.is_verified = True
    user.save()
    message = u'账号激活成功，可以进行<a href=\"' + DOMAIN + u'/api/login\">登录</a>操作'
    # return render(request, 'common/success.html', {'reason': message})

    return HttpResponse(message, status=200)
