from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Users,HIS
from .serializers import HISSerialize,UsersSerializer,UserStatusSerial,UserUpdateApplySerial
from rest_framework.parsers import JSONParser
from datetime import timedelta,date
from django.utils import timezone
from datetime import datetime
from datetime import timedelta,date
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
DOMAIN = 'http://192.168.43.184:8000'        # 网站运行域
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
            #add is verified
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

def super_user_list_rent(request):
    if request.method == 'POST':
        print(request)
        print('superuser come to check users lists')
        #if(check_password('0000', request.body.decode("utf-8"))):
        if(True):
            query_set = Users.objects.all()
            print(query_set)
            serializer = UserStatusSerial(query_set, many=True)
            print(serializer.data)
            temp=sorted(serializer.data, key=lambda t: t['is_apply_b'], reverse=True)
            print('this',type(temp))
            new_list = [ dd for dd in temp if not dd['is_staff'] is 0]
            new_list = [dd for dd in new_list if not dd['is_staff'] is 1]
            #add is verified
            #temp = dict(filter(key=lambda t: t['is_staff'] >= 2, temp))
            #print(sorted(serializer.data.values("is_apply_a")))
            print("get!!!! mota!")
            print(temp)
            return JsonResponse({"list":list(json.loads(json.dumps(new_list)))}, status=200)
        else:
            return HttpResponse({"error":"you are not super user"}, status=500)


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
                #record = Users.objects.get(userid=data['userid'])  super noti
                #UserStatusSerial().down_noti(record)
                return JsonResponse({'up': ' 병시나'}, status=201)

            else:
                return HttpResponse({"error": "you are not super user"}, status=500)


@csrf_exempt
def user_apply_status_up(request):

    if request.method == 'POST':
        if True:
            data = JSONParser().parse(request)
            print(data)

            search_name = data['userid']
            try:
                obj = Users.objects.get(userid=data['userid'])
            except:
                return JsonResponse({'status': 'false', 'message': "no such user"}, status=500)

            record = Users.objects.get(userid=data['userid'])
            UsersSerializer().user_apply_status_up(record,data['reason_pro'])
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
                #record = Users.objects.get(userid=data['userid'])
                #UserStatusSerial().down_noti(record)
                return JsonResponse({'뭐래': '쿠켈켈'}, status=201)

            else:
                return HttpResponse({"error": "you are not super user"}, status=500)



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
def send_user_status(request):

    if request.method == 'POST':
        #print(JSONParser().parse(request))
        print(request.body.decode("utf-8"))
        obj = Users.objects.get(userid=request.body.decode("utf-8"))
        #print(JSONParser(request))
       # serializer = UsersSerializer(obj)

        return JsonResponse({'is_staff':obj.is_staff,'rent_status':obj.rent_status,'is_rent':obj.is_rent}, safe=False)


@csrf_exempt
def update_user_status(request):
    print('this is user status')
    if request.method == 'POST':

        data = JSONParser().parse(request)
        print(data)
        record = Users.objects.get(userid=data['userid'])
        UserStatusSerial().update_rent_status(record, data['is_rent'],data['rent_status'])
        try:
            UserStatusSerial().update_rent_date(record, data['rent_start'], data['rent_end'])
            UserStatusSerial().user_rent_apply(record,data['equip_id'],data['equip_name'])
        except:
             print("no start")

        return JsonResponse({'update':"success"}, safe=False)

@csrf_exempt
def  user_return_apply(request):

    if request.method == 'POST':
        data = JSONParser().parse(request)
        record = Users.objects.get(userid=data['userid'])
        UserStatusSerial().rent_status_to2(record,data['equipid'])

@csrf_exempt
def user_history(request):


        if request.method == 'POST':
            print('history')

            try:
                data = JSONParser().parse(request)
            except:
                return HttpResponse("deny mounted .", status=200)


            the_user = Users.objects.get(userid=data['user_id'])
            reservations = the_user.history_e.all()
            result = list([])
            print('a')
            query_set = the_user.history_e.all()
            print(query_set)
            serializer = HISSerialize(query_set, many=True)

            return JsonResponse({"list": list(json.loads(json.dumps(serializer.data)))}, status=200)


@csrf_exempt
def allow_return(request):
    #
    if request.method == 'POST':
        data = JSONParser().parse(request)
        the_user = Users.objects.get(userid=data['userid'])
        #UserStatusSerial().allow_return(the_user)

        data = {"equip_name": data['equip_name'], "equip_id": data['equip_id'],
                #"borrow_from":the_user.rent_start
                "borrow_from": data['rent_start'] , "borrow_till": data['rent_exp'],}
        print("this is data", data)
        serializer = HISSerialize(data=data)
        if serializer.is_valid():
            id = serializer.save()
            query_set = HIS.objects.all()
            obj = HIS.objects.get(id=id.id)
            print(obj)
            the_user.history_e.add(obj)
            print('to here ADD SUCCESS', obj)
        else:
            print(serializer.errors)
            return JsonResponse({'update': "success"}, safe=False)
    return JsonResponse({'update': "nope"}, safe=False)


@csrf_exempt
def  user_rent_apply(request):

    if request.method == 'POST':
        data = JSONParser().parse(request)
        print(data)
        record = Users.objects.get(userid=data['userid'])
        print('here！！！')
        UserStatusSerial().user_rent_apply(record,data['equipid'],data['equip_name'])
        print('here2')
        record = Users.objects.get(userid=data['provider_id'])
        print('here3')
        UserStatusSerial().user_rent_apply_to_provider(record)
        print('here4')
        record = Users.objects.get(userid=data['provider_id'])##superuser_id
        print('here5')
        UserStatusSerial().user_rent_apply_to_super(record)
        return  JsonResponse({"success":"apply success"}, status=200)



@csrf_exempt
def  user_get_your_status(request):

    if request.method == 'POST':
        obj = Users.objects.get(userid=request.body.decode("utf-8"))
        serializer = UsersSerializer(obj)

        start_date = timezone.now().date()
        end_date = start_date - timedelta(days=1)

        if  serializer.data['is_rent']:
            print(serializer.data)
            print(serializer.data['rent_end'])
            exp_day = datetime.strptime(serializer.data['rent_end'], '%Y/%m/%d').date()
            start_day = datetime.strptime(serializer.data['rent_start'], '%Y/%m/%d').date()
            print(exp_day)
            today = timezone.now().date()
            till_startday=(today-start_day).days
            print(till_startday)
            day=(exp_day - today).days
            if till_startday<0:
                return JsonResponse({"days": till_startday, "info": serializer.data}, status=200)
            elif day>=0:
                return JsonResponse({"days":day ,"info":serializer.data}, status=200)
            else:
                day=day+0.3
                return JsonResponse({"days":-day ,"info":serializer.data}, status=200)
        else:
            return JsonResponse({"days":"availabe","info":serializer.data}, status=200)





@csrf_exempt
def history_to_user(request):
    #李同学请看，在这个函数你会收到三个参数1，设备id，2用户名，3用户id 将其一次排入waitinglist 中 并保证申请过的id无法在申请
    #最好也能实现一下 waitinglist的删除
    print("this is post",request)
    try:
        data = JSONParser().parse(request)
    except:
        return HttpResponse("deny mounted .", status=200)

    try:
        the_user = Users.objects.get(id=data['user_id'])

    except Users.DoesNotExist:
        return HttpResponse("The USER you want to operate does not exist.", status=200)

    if request.method =='POST':
        temp = datetime.datetime.strptime(data['rent_start'], '%Y/%m/%d')
        data={"user_id":data['user_id'], "name":data['equip_name'], "borrow_from":temp,"borrow_til":datetime.now(),}
        print("this is data",data)
        serializer = HISSerialize(data=data)
        print('fuck')
        if serializer.is_valid():
            print('to here fianl')
            serializer.save()
            query_set = HIS.objects.all()
            print('a',len(query_set))
            serializer =HISSerialize(query_set, many=True)
            print('ddd',serializer.data)
            obj=HIS.objects.get(id=len(query_set))
            print(obj)
            the_user.waiting_list.add(obj)
            print('to here ADD SUCCESS',obj)

    if request.method =='PATCH':

        print('waiting_list')
        try:
            data = JSONParser().parse(request)
        except:
            return HttpResponse("deny mounted .", status=200)

        try:
            his_item = HIS.objects.get(id=data['equipid'])
        except HIS.DoesNotExist:
            return HttpResponse("The equip you want to operate does not exist.", status=200)
        query_set = his_item.waiting_list.all()
        serializer = HISSerialize(query_set, many=True)
        return JsonResponse({"list": list(json.loads(json.dumps(serializer.data)))}, status=200)

    return JsonResponse({"sucess":"?"})

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
            name=Users.objects.get(userid=data['userid'])
            print(name.username)
            return JsonResponse({"token":obj.password,"userid":data['userid'],'username':name.username}, status=200)


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
        print(data)
        print(type(data))

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
        token = token_confirm.generate_validate_token(data['userid'])
        token_url = '/'.join([DOMAIN, 'activate', token])

        message = "\n".join([u'{0},欢迎加入设备租借系统'.format(['userid']),
                             u'请访问该链接，完成用户验证:',
                             token_url])
        send_mail(u'注册用户验证信息', message, '1326742692@qq.com', [data['email']], fail_silently=False)

        return HttpResponse({'success':'success'}, status=200)

    return HttpResponse({'data':'fail'}, status=400)



@csrf_exempt
def user_verified(request, token):
    #当用户在自己的邮箱点击 认证token时会启动该函数 并将该user的 is_verified转换为 true
    try:
        username = token_confirm.confirm_validate_token(token)
    except:       # 令牌过期
        username = token_confirm.remove_validate_token(token)
        users = Users.objects.filter(userid=username)
        for user in users:
            user.delete()  # 删除注册用户
        return HttpResponse(
            u'对不起，验证链接已经过期，请重新注册</a>',
            status=200
        )

    try:
        user = Users.objects.get(userid=username)
    except Users.DoesNotExist:
        return HttpResponse(u"对不起，您所验证的用户不存在，请重新注册", status=400)
    user.is_verified = True
    user.is_active=True
    user.is_staff=3
    user.save()
    message = u'账号激活成功，可以进行登录</a>操作'
    # return render(request, 'common/success.html', {'reason': message})

    return HttpResponse(message, status=400)


@csrf_exempt
def data_ana(request):

    if request.method == 'GET':
        try:
            query_set = HIS.objects.all()
            historys =HISSerialize(query_set, many=True)
            print(historys.data)
            data={}
            result={}
            print(type(data))
            for history in  query_set:
                print(history.equip_id)
                start_day = datetime.strptime(history.borrow_from, '%Y/%m/%d').date()
                print('??')
                exp_day = datetime.strptime(history.borrow_till, '%Y/%m/%d').date()
                day = (exp_day - start_day).days
                print('??')
                if history.equip_id in  data.keys():
                    data[history.equip_id].append(day)
                else:
                    print('?')
                    dict = {history.equip_id: [day]}
                    data.update(dict)
                    print('kk')
            for key ,value in data.items():
                print(str(key))
                print(sum(value) / len(value))
                dict={key:sum(value) / len(value)}
                result.update(dict)
        except:
            return JsonResponse({key:result[key] for key in sorted(result.keys())}, status=200)

    if request.method == 'POST':
        try:
            query_set = HIS.objects.all()
            historys = HISSerialize(query_set, many=True)
            print(historys.data)
            data = {}
            result = {}
            print(type(data))
            for history in query_set:
                print(history.equip_id)
                start_day = datetime.strptime(history.borrow_from, '%Y/%m/%d').date()
                print('??')
                exp_day = datetime.strptime(history.borrow_till, '%Y/%m/%d').date()
                day = (exp_day - start_day).days
                print('??')
                if history.equip_id in data.keys():
                    data[history.equip_id].append(day)
                else:
                    print('?')
                    dict = {history.equip_id: [day]}
                    data.update(dict)
                    print('kk')
            for key, value in data.items():
                print(str(key))
                print(sum(value) / len(value))
                dict = {key: len(value)}
                result.update(dict)

            return JsonResponse({key: result[key] for key in sorted(result.keys())}, status=200)


        except:


            return JsonResponse({"list":"D"}, status=200)
    return JsonResponse({"list": "D"}, status=200)


