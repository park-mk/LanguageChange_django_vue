from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Users
from .serializers import UsersSerializer,UserStatusSerial,UserUpdateApplySerial
from rest_framework.parsers import JSONParser
from datetime import timedelta,date
from django.utils import timezone

from django.utils.dateparse import parse_datetime
from django.contrib.auth.hashers import make_password,check_password
import json

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

#这是为了测试时临时加user 用的函数
def super_user_list(request):
    if request.method == 'POST':
        print(request)
        print('superuser come to check users lists')
        #if(check_password('0000', request.body.decode("utf-8"))):
        if(True):
            query_set = Users.objects.all()
            print(query_set)
            serializer = UserStatusSerial(query_set, many=True)
            print(serializer.data)
            temp=sorted(serializer.data, key=lambda t: t['is_apply_a'], reverse=True)
            print('this',type(temp))
            new_list = [ dd for dd in temp if not dd['is_staff'] is 0]
            new_list = [dd for dd in new_list if not dd['is_staff'] is 1]
            #temp = dict(filter(key=lambda t: t['is_staff'] >= 2, temp))
            #print(sorted(serializer.data.values("is_apply_a")))
            print("get!!!! mota!")
            print(temp)
            return JsonResponse({"list":list(json.loads(json.dumps(new_list)))}, status=200)
        else:
            return HttpResponse({"error":"you are not super user"}, status=500)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        data['password'] = make_password(data['password'])
        serializer = UsersSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)




def create_user(data):
    print('?2')
    print('?2')
    data['password'] = make_password(data['password'])
    serializer = UsersSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return JsonResponse(serializer.data, status=201)
    return JsonResponse(serializer.errors, status=400)


#这是管理者删除user的函数
@csrf_exempt
def super_del_user(request):
    if request.method == 'DELETE':
        record = Users.objects.get(userid='0005')
        UsersSerializer().delete(record)
        return JsonResponse({'SUCCESS': 'SUCCE??SS'}, status=201)
    if request.method == 'POST':
        data = JSONParser().parse(request)
        if True: #(check_password('0000', data['token'])):
            search_name = data['userid']
            try:

                obj = Users.objects.get(userid=data['userid'])
                print(obj)

            except:
                return JsonResponse({'status':'false','message':"no such user"}, status=500)
            print('i will delete2', search_name)
            UsersSerializer().delete(obj)
            return JsonResponse({'d':'success'}, status=200)
        else:
            return HttpResponse({"error": "you are not super user"}, status=500)

@csrf_exempt
def super_update_user(request):

    if request.method == 'POST':
        if True:
            data = JSONParser().parse(request)
            print(data)
            if (check_password('0000', data['token'])):
                print('fuck you')
                search_name = data['userid']
                try:
                    obj = Users.objects.get(userid=data['userid'])
                except:
                    return JsonResponse({'status': 'false', 'message': "no such user"}, status=500)

                record = Users.objects.get(userid=data['userid'])
                UserStatusSerial().upgrade_status(record)
                return JsonResponse({'up': ' 병시나'}, status=201)

            else:
                return HttpResponse({"error": "you are not super user"}, status=500)




@csrf_exempt
def super_downdate_user(request):

    if request.method == 'POST':
        if True:

            data = JSONParser().parse(request)

            if (check_password('0000', data['token'])):

                search_name = data['userid']

                try:
                    obj = Users.objects.get(userid=data['userid'])
                except:
                    return JsonResponse({'status': 'false', 'message': "no such user"}, status=500)

                record = Users.objects.get(userid=data['userid'])
                UserStatusSerial().downgrade_status(record)
                return JsonResponse({'뭐래': '안보이냐'}, status=201)

            else:
                return HttpResponse({"error": "you are not super user"}, status=500)


@csrf_exempt
def super_deny_apply(request):

    if request.method == 'POST':
        if True:

            data = JSONParser().parse(request)

            if (check_password('0000', data['token'])):

                search_name = data['userid']

                try:
                    obj = Users.objects.get(userid=data['userid'])
                except:
                    return JsonResponse({'status': 'false', 'message': "no such user"}, status=500)

                record = Users.objects.get(userid=data['userid'])
                UserStatusSerial().deny_apply(record)
                return JsonResponse({'뭐래': '쿠켈켈'}, status=201)

            else:
                return HttpResponse({"error": "you are not super user"}, status=500)
@csrf_exempt
def super_view_rent_user(request):

    if request.method == 'POST':
        if True:
        #if(check_password('0000', request.body.decode("utf-8"))):
            #data = JSONParser().parse(request)
           # search_name = data['userid']
            obj = Users.objects.filter(is_apply_b=True)
            obj2 = Users.objects.filter(is_rent=True)
            result = list(obj) + list(obj2)
            serializer = UserStatusSerial(result, many=True)
            print(serializer.data)

            return JsonResponse({"error":"you are not super user"}, status=200)

        else:
            return HttpResponse({"error":"you are not super user"}, status=500)

@csrf_exempt
def super_view_rent_user_info(request):

    if request.method == 'POST':
        data = JSONParser().parse(request)
        if (check_password('0000', data['token'])):
            obj = Users.objects.get(userid=data['userid'])
            serializer = UserUpdateApplySerial(obj)
            print(serializer.data)

            return JsonResponse(serializer.data, status=200)

        else:
            return HttpResponse({"error":"you are not super user"}, status=500)

@csrf_exempt
def user_apply_rent(request):

    if request.method == 'POST':
        data = JSONParser().parse(request)
        if (check_password('0000', data['token'])):
            obj = Users.objects.get(userid=data['userid'])
            serializer = UserUpdateApplySerial(obj)
            print(serializer.data)

            return JsonResponse(serializer.data, status=200)

        else:
            return HttpResponse({"error":"you are not super user"}, status=500)


@csrf_exempt
def send_user_status(request):

    if request.method == 'POST':
        #print(JSONParser().parse(request))
        print(request.body.decode("utf-8"))
        obj = Users.objects.get(userid=request.body.decode("utf-8"))
        #print(JSONParser(request))
       # serializer = UsersSerializer(obj)
        return JsonResponse({'is_staff':obj.is_staff}, safe=False)

@csrf_exempt
def  user_get_your_status(request):

    if request.method == 'POST':
        obj = Users.objects.get(userid=request.body.decode("utf-8"))
        serializer = UsersSerializer(obj)
        print(obj)
        start_date = timezone.now().date()
        end_date = start_date - timedelta(days=1)
        if  serializer.data['is_rent']:
            exp_day = parse_datetime(serializer.data['created_at']).date()
            today = timezone.now().date()
            print((exp_day - today).days)
            day=(exp_day - today).days
            print(serializer.data['created_at'])
            return JsonResponse({"days":day}, status=200)
        else:

            return JsonResponse({"days":"availabe"}, status=200)




@csrf_exempt
def login(request):

    if request.method == 'POST':

        print('fuck')
        print(request.POST)

        data = JSONParser().parse(request)
        print(data)
        search_name = data['userid']
        print('data')
        try:
            obj = Users.objects.get(userid=search_name)
        except:

            return JsonResponse({'status':'false','message':"no such user"}, status=500)


        if check_password(data['password'],obj.password):
            # if verified =false return haven't verified
            print('to heddddre')
            return JsonResponse({"token":obj.password,"userid":data['userid']}, status=200)


        else:
            print("fail!!")
            return HttpResponse(status=401)


    return render(request, 'Users/login.html')


@csrf_exempt
def register_mail_post(request):
    if request.method == 'POST':
        #当在 api／register中有post 请求 输入{username: password: email :}d的时候 向指定的email发送认证email 并保证该email 可以重新
        #跑动 新的函数 def user_verified

        # invitation: 邀请码 只有有正确邀请码的注册用户才可以成为管理员
        # is_provider: 是否注册成为提供者(可提供打勾选项)

        # 获取用户注册数据
        data = JSONParser().parse(request)
        # 验证是否注册过
        print('?')
        is_username_repeated = Users.objects.filter(userid=data['userid'])
        is_email_repeated = Users.objects.filter(email=data['email'])
        if is_username_repeated:
            return HttpResponse('该用户名已经被注册过，请重新注册', status=200)
        if is_email_repeated:
            return HttpResponse('该邮件已经被注册过，请重新注册', status=200)

        # 验证是否注册管理员（邀请码的正确性）

        print('?')
        # 不能同时成为两个身份


        # 确认注册信息有效后，插入数据

        create_user(data)

        # 邮箱验证
        token = token_confirm.generate_validate_token(data['username'])
        token_url = '/'.join([DOMAIN, 'activate', token])
        message = "\n".join([u'{0},欢迎加入XX'.format(['username']),
                             u'请访问该链接，完成用户验证:',
                             token_url])
        send_mail(u'注册用户验证信息', message, '1326742692@qq.com', [data['email']], fail_silently=False)

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
