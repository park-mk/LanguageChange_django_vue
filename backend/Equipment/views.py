from .models import Equip, LIST,HIS,GRADE
from .serializers import   GRADESerialize,HISSerialize,WaitingSerializer,EquipSerializer,EquipStatusSerializer,EquipONSerializer,EquipDesSerializer,EquipRentSerializer,EquipRentUserSerializer
from rest_framework.parsers import JSONParser
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import make_password,check_password
import json
from datetime import datetime
from datetime import timedelta,date
from django.utils import timezone
from django.utils.dateparse import parse_datetime
from django.db.models.functions import (
    ExtractDay, ExtractMonth, ExtractYear
)
from .utils import add_print_date, date2count
import datetime
# Create your views here.

@csrf_exempt
def equip_list(request):
    if request.method == 'POST':


        print('superuser come to check users lists')
        if True:#(check_password('0000', request.body.decode("utf-8"))):
            query_set = Equip.objects.all()
            serializer =EquipStatusSerializer(query_set, many=True)
            for query in query_set:
                se =EquipStatusSerializer(query)
                EquipStatusSerializer().is_apply_to(query,wait_list_check(se.data['id']))
                print(se.data)
            temp = sorted(serializer.data, key=lambda t: t['is_apply'], reverse=True)

            return JsonResponse({"list":list(json.loads(json.dumps(temp)))}, status=200)
        else:
            return HttpResponse({"error": "you are not super user"}, status=500)

    elif request.method == 'PUT':
        print('to here')
        data = JSONParser().parse(request)
        print(data)

        serializer = EquipSerializer(data=data)
        print(serializer)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

    if request.method == 'PATCH':


        print('provider come to check his equip')
        if True:  # (check_password('0000', request.body.decode("utf-8"))):
            query_set = Equip.objects.all()
            serializer = EquipStatusSerializer(query_set, many=True)
            for query in query_set:
                se = EquipStatusSerializer(query)
                EquipStatusSerializer().is_apply_to(query, wait_list_check(se.data['id']))
                print(se.data)
            temp = sorted(serializer.data, key=lambda t: t['is_rent'], reverse=True)

            new_list = [dd for dd in temp if dd['provider_id'] == request.body.decode("utf-8")]
            print(new_list)
            return JsonResponse({"list": list(json.loads(json.dumps(new_list)))}, status=200)
        else:
            return HttpResponse({"error": "you are not super user"}, status=500)



@csrf_exempt

def wait_list_check(equip_id):



        print('lets check ',equip_id)
        equip_item = Equip.objects.get(id=equip_id)
        # EquipSerializer().return_equip_check(equip_item)
        reservations = equip_item.waiting_list.all()

        for reservation in reservations:

            serial = WaitingSerializer(reservation)
            print(serial.data['apply_succes'])
            if serial.data['apply_succes']==False:
                return True
                break

        return False

@csrf_exempt
def wujun_is(request):
    if request.method == 'GET':

        data = JSONParser().parse(request)
        equip_item = Equip.objects.get(id=data['equip_id'])
        try:
            EquipSerializer().is_rent_up( equip_item,data['is_rent'])
        except:
            pass
        try:
            EquipSerializer().is_rent_up(equip_item, data['is_return'])
        except:
            pass
        try:
            EquipSerializer().is_gelai_up(equip_item, data['is_gelai'])
        except:
            pass


        return JsonResponse({"congra": 'tulation'}, status=200)


@csrf_exempt
def equip_on_list(request):
    if request.method == 'GET':

        print('user come to check users lists')
        if True:  # (check_password('0000', request.body.decode("utf-8"))):
            query_set = Equip.objects.all()
            print(query_set)
            serializer = EquipONSerializer(query_set, many=True)
            print(query_set)
            new2_list = [dd for dd in serializer.data if dd['is_active'] is True]
            new_list = new2_list
            print('this',new_list)
            return JsonResponse({"list": list(json.loads(json.dumps(new_list)))}, status=200)


@csrf_exempt
def equip_rent_list(request):
    print('aa')
    if request.method == 'POST':

        print('superuser come to check users lists')
        if True:#(check_password('0000', request.body.decode("utf-8"))):
            query_set = Equip.objects.all()
            print(query_set)
            serializer = EquipRentSerializer(query_set, many=True)
            print(serializer.data)
            temp = sorted(serializer.data, key=lambda t: t['is_apply'], reverse=True)
            print('this', type(temp))
            new_list = [dd for dd in temp if dd['is_apply'] is True]
            new2_list = [dd for dd in temp if  dd['is_rent'] is True]
            new_list=new_list+new2_list
            # temp = dict(filter(key=lambda t: t['is_staff'] >= 2, temp))
            # print(sorted(serializer.data.values("is_apply_a")))
            print("get!!!! mota!")
            print(temp)
            return JsonResponse({"list": list(json.loads(json.dumps(new_list)))}, status=200)

        else:
            return HttpResponse({"error": "you are not super user"}, status=500)


@csrf_exempt
def return_equip(request):
    if request.method == 'POST':
        print(request.body.decode("utf-8"))
        print('??')
        record = Equip.objects.get(id=request.body.decode("utf-8"))
        EquipSerializer().return_equip(record)
        print(record.is_return ,'this is ')
    return JsonResponse({"return":" user_success"}, status=200)

@csrf_exempt
def return_equip_check(request):
    if request.method == 'POST':
        data = JSONParser().parse(request)
        equip_item = Equip.objects.get(id=data['equip_id'])
        #EquipSerializer().return_equip_check(equip_item)
        reservations = equip_item.waiting_list.all()
        print(reservations.count(), 'resereve')
        print(reservations)
         #equip_item.waiting_list.remove(serial.data['id'])
        print('this is data',data)
        for reservation in reservations:
            print('터져', reservation)
        for reservation in reservations:
            serial = WaitingSerializer(reservation)
            print(data['user_id'])
            if serial['user_id'] ==data['user_id']:
                equip_item.waiting_list.remove(serial.data['id'])
                history = {"user_id": data['user_id'], "user_name": data['user_name'],
                           "rent_start": data['rent_start'],
                           "rent_exp":data['rent_exp'], "reason": serial.data['reason']}
                h_serializer = HISSerialize(data=history)
                if h_serializer.is_valid():
                    id=h_serializer.save()
                    query_set = HIS.objects.all()
                    obj = HIS.objects.get(id=id.id)
                    equip_item.history_list.add(obj)  # ADD
        return HttpResponse("return and add history list successfully.", status=200)

@csrf_exempt
def equip_rent_list_specific(request,id):
    print('aa')
    if request.method == 'POST':

        print('superuser come to check users lists')
        if True:#(check_password('0000', request.body.decode("utf-8"))):
            query_set = Equip.objects.all()
            print(query_set)
            serializer = EquipRentSerializer(query_set, many=True)
            print(serializer.data)
            temp = sorted(serializer.data, key=lambda t: t['is_apply'], reverse=True)
            print('this', type(temp))
            new_list = [dd for dd in temp if dd['is_apply'] is True]
            new2_list = [dd for dd in temp if  dd['is_rent'] is True]
            new_list=new_list+new2_list
            # temp = dict(filter(key=lambda t: t['is_staff'] >= 2, temp))
            # print(sorted(serializer.data.values("is_apply_a")))
            print("get!!!! mota!")
            print(temp)
            return JsonResponse({"list": list(json.loads(json.dumps(new_list)))}, status=200)

        else:
            return HttpResponse({"error": "you are not super user"}, status=500)

@csrf_exempt
def provider_add_list(request):
    if request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = EquipSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

@csrf_exempt
def equip_borrow_user_info(request):

    if request.method == 'POST':
        data = JSONParser().parse(request)
        print(data)
        if True :#(check_password('0000', data['token'])):

            try:
                obj = Equip.objects.get(id=data['equipid'])
            except:
                return JsonResponse({'status': 'false', 'message': "no such user"}, status=500)
            serializer = EquipRentUserSerializer(obj)
            print('wkfrka')
            return JsonResponse(serializer.data, status=201)




@csrf_exempt
def equip(request,id):
    #print(id)
    obj = Equip.objects.get(id=id)

    if request.method == 'GET':
        serializer = EquipSerializer(obj)
        return JsonResponse(serializer.data, safe=False)




@csrf_exempt
def provider_add_list(request):
    if request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = EquipSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)


@csrf_exempt
def deny_equip(request):
    if request.method == 'POST':

        data = JSONParser().parse(request)
        record = Equip.objects.get(id=data['equipid'])
        EquipStatusSerializer().deny_apply(record) #ehfdkdhk
        history = HIS.objects.get(id=data['equipid'])


        return JsonResponse({"yes":"denied"}, status=200)


@csrf_exempt
def accept_rent_equip(request):
    if request.method == 'POST':
        data = JSONParser().parse(request)
        record = Equip.objects.get(id=data['equipid'])
        EquipStatusSerializer().accept_apply(record)
        return JsonResponse({"yes":"accepted"}, status=200)


@csrf_exempt
def deny_rent_equip(request):
    if request.method == 'POST':
        data = JSONParser().parse(request)
        record = Equip.objects.get(id=data['equipid'])
        EquipStatusSerializer().deny_apply(record)
        return JsonResponse({"yes":"denied"}, status=200)

@csrf_exempt
def provider_get_equip(request):
    if request.method == 'POST':
        obj = Equip.objects.get(userid=request.body.decode("utf-8"))
        data = JSONParser().parse(request)
        record = Equip.objects.get(id=data['equipid'])
        EquipStatusSerializer().deny_apply(record)
        return JsonResponse({"yes":"denied"}, status=200)


@csrf_exempt
def provider_update_equip(request,id):
    if request.method == 'GET':
        data = JSONParser().parse(request)
        return JsonResponse(data, status=201)

    if request.method == 'POST':
        data = JSONParser().parse(request)
        record = Equip.objects.get(id=id)
        EquipSerializer().update(record,data)
        return JsonResponse({'s':'s'}, status=201)


@csrf_exempt
def provider_del_equip(request):
    if request.method == 'POST':
        print('here')
        data = JSONParser().parse(request)
        record = Equip.objects.get(id=data['equipid'])
        EquipSerializer().delete(record)
        return JsonResponse({'SUCCESS':'SUCCE??SS'}, status=201)

@csrf_exempt
def provider_on_equip(request,id):
    if request.method == 'GET':
        record = Equip.objects.get(id=id)
        print('on')
        EquipSerializer().on(record)
        return JsonResponse({'SUCCESS':'SUCCESS'}, status=201)

@csrf_exempt
def provider_off_equip(request,id):
    if request.method == 'GET':
        record = Equip.objects.get(id=id)
        EquipSerializer().off(record)
        return JsonResponse({'SUCCESS':'SUCCESS'}, status=201)

def super_on_equip(request,id): #ehfdkdhk
    if request.method == 'GET':
        record = Equip.objects.get(id=id)
        print('on')
        EquipSerializer().activate(record)
        return JsonResponse({'SUCCESS':'SUCCESS'}, status=201)

def super_on_equip(request,id): #ehfdkdhk
    if request.method == 'GET':
        record = Equip.objects.get(id=id)
        print('on')
        EquipSerializer().unactivate(record)
        return JsonResponse({'SUCCESS':'SUCCESS'}, status=201)






@csrf_exempt
def equip_history(request):

    if request.method == 'POST':
        print('history')

        try:
            data = JSONParser().parse(request)
        except:
            return HttpResponse("deny mounted .", status=200)

        try:
            equip_item = Equip.objects.get(id=data['equipid'])

        except Equip.DoesNotExist:
            return HttpResponse("The equip you want to operate does not exist.", status=200)
        reservations = equip_item.history_list.all()
        result=list([])
        query_set = equip_item.history_list.all()
        print(query_set)
        serializer = HISSerialize(query_set, many=True)

        return  JsonResponse({"list":list(json.loads(json.dumps(serializer.data)))}, status=200)


@csrf_exempt
def equip_waiting_list(request):
    if request.method == 'POST':
        print('waiting_list')
        try:
            data = JSONParser().parse(request)
        except:
            return HttpResponse("deny mounted .", status=200)

        try:
            equip_item = Equip.objects.get(id=data['equipid'])
        except Equip.DoesNotExist:
            return HttpResponse("The equip you want to operate does not exist.", status=200)
        query_set = equip_item.waiting_list.all()
        serializer = WaitingSerializer(query_set, many=True)
        print(len(query_set))
        return JsonResponse({"list": list(json.loads(json.dumps(serializer.data)))}, status=200)

@csrf_exempt
def super_allow_equip_rent(request):
    if request.method == 'POST':
        print('waiting_list')
        try:
            data = JSONParser().parse(request)
        except:
            return HttpResponse("deny mounted .", status=200)

        try:
            equip_item = Equip.objects.get(id=data['equipid'])

        except Equip.DoesNotExist:
            return HttpResponse("The equip you want to operate does not exist.", status=200)
        EquipRentSerializer().is_rent(equip_item)  # ehfdkdhk
        record = LIST.objects.get(id=data['id'])
        print(record)
        WaitingSerializer().allow(record)
        return JsonResponse({"allow": "allowed!"}, status=200)
    if request.method == 'PUT':
        print('waiting_list')
        try:
            data = JSONParser().parse(request)
        except:
            return HttpResponse("deny mounted .", status=200)

        try:
            equip_item = Equip.objects.get(id=data['equipid'])

        except Equip.DoesNotExist:
            return HttpResponse("The equip you want to operate does not exist.", status=200)

        record = LIST.objects.get(id=data['id'])
        WaitingSerializer().deny(record)
        return JsonResponse({"deny": "denied!"}, status=200)


@csrf_exempt
def equip_grading(request):
    try:
        data = JSONParser().parse(request)
    except:
        return HttpResponse("deny mounted .", status=200)

    try:
        equip_item = Equip.objects.get(id=data['equip_id'])

    except Equip.DoesNotExist:
        return HttpResponse("The equip you want to operate does not exist.", status=200)
    print('to here')
    if request.method == 'POST':
        user_id = data['user_id']
        user_name = data['user_name']
        grade=data['grade']
        data = {"user_id": user_id, "user_name": user_name, "grade": grade, "comment":data['comment']}
        serializer = GRADESerialize(data=data)
        if serializer.is_valid():
            id=serializer.save()
            query_set = GRADE.objects.all()
            serializer = GRADESerialize(query_set, many=True)
            obj = GRADE.objects.get(id=id.id)
            equip_item.grade_list.add(obj)
            return HttpResponse("success", status=200)
        print(serializer.errors)
        return HttpResponse("fail", status=200)

    if request.method == 'PATCH':
        query_set = GRADE.objects.all()
        serializer = GRADESerialize(query_set, many=True)

        print("dd",equip_item.grade_list.all())
        totals=equip_item.grade_list.all()
        total=0
        count=0
        for grade in totals:
            count=count+1
            total=total+grade.grade
        total=total/count

        return HttpResponse(total, status=200)

@csrf_exempt
def user_to_waitinglist(request):
    #李同学请看，在这个函数你会收到三个参数1，设备id，2用户名，3用户id 将其一次排入waitinglist 中 并保证申请过的id无法在申请
    #最好也能实现一下 waitinglist的删除
    print("this is user tp witlist ",request)
    try:
        data = JSONParser().parse(request)
    except:
        return HttpResponse("deny mounted .", status=200)

    try:
        equip_item = Equip.objects.get(id=data['equipid'])

    except Equip.DoesNotExist:
        return HttpResponse("The equip you want to operate does not exist.", status=200)

    date_unavailable_list = []      # 已占用的日期列表：形式['2020/7/8', '2020/7/9', ]
    if request.method == 'POST': #有效性
        print("???")
        reservations = equip_item.waiting_list.all()
        print(reservations.count(),'resereve')
        print(reservations)
        for reservation in reservations:
            print('터져',reservation)
        for reservation in reservations:
            serial = WaitingSerializer(reservation)
            now_time = datetime.datetime.now()
            exp=int(serial.data['rent_exp'][0:4])*10000+int(serial.data['rent_exp'][5:7])*100+int(serial.data['rent_exp'][8:10])
            print(serial.data['id'],"this is id")
            now=now_time.year*10000+now_time.month*100+now_time.day*1
            print(exp,now)
            if(exp<now):
                equip_item.waiting_list.remove(serial.data['id'])
                print('remove success')
                history = { "user_id": serial.data['user_id'], "user_name":serial.data['user_name'], "rent_start": serial.data['rent_start'],
                        "rent_exp": serial.data['rent_exp'], "reason":serial.data['reason']}
                print(history)
                h_serializer = HISSerialize(data=history)
                if h_serializer.is_valid():
                    print('?')
                    h_serializer.save()
                    query_set = HIS.objects.all()
                    print(len(query_set))
                    serializer = HISSerialize(query_set, many=True)
                    print(serializer.data)
                    obj = HIS.objects.get(id=len(query_set))
                    print(obj)
                    equip_item.history_list.add(obj) #ADD
        print('fuck')
        return HttpResponse("Quit from waiting list successfully.", status=200)


    if request.method =='PATCH':
        reservations = equip_item.waiting_list.all()
        print(reservations.count(), 'resereve')
        print(reservations)
        for reservation in reservations:
            print('터져', reservation)
        for reservation in reservations:
            serial = WaitingSerializer(reservation)
            print('last',serial.data)
            start = datetime.datetime.now()
            exp = int(serial.data['rent_exp'][0:4]) * 10000 + int(serial.data['rent_exp'][5:7]) * 100 + int(
            serial.data['rent_exp'][8:10])
            print(serial.data['id'], "this is id")
            from_date =datetime.datetime.strptime(serial.data['rent_start'][0:10], '%Y-%m-%d')
            to_date = datetime.datetime.strptime(serial.data['rent_exp'][0:10], '%Y-%m-%d')
            print(from_date,'haha')
            print((to_date -from_date).days)
            day = (to_date -from_date).days
            date_time = from_date.strftime("%Y/%m/%d")
            temp=datetime.datetime.strptime(date_time, '%Y/%m/%d')
            print("date and time:", date_time)
            for _ in range(day+1):
                date_time = temp.strftime("%Y/%m/%d")
                print(date_time)
                date_unavailable_list.append(date_time)
                temp=temp + timedelta(days=1)
        print('end')
        return JsonResponse({"sucess": date_unavailable_list})

    if request.method == 'PUT':
        user_id = data['user_id']
        user_name=data['user_name']
        reason = data['reason']
        phone = data['phone_number']
        reason = reason + '#' + phone
        start_time = data['start'].strip()  # 格式: '2020/7/8'
        end_time = data['end'].strip()
        start_time = start_time.split('/')
        end_time = end_time.split('/')
        # 检查是否该时段有人占用
        time_list = []
        add_print_date(year_from=int(start_time[0]),
                       month_from=int(start_time[1]),
                       day_from=int(start_time[2]),
                       year_to=int(end_time[0]),
                       month_to=int(end_time[1]),
                       day_to=int(end_time[2]),
                       list_of_date=time_list)
        count=1,
        for date in time_list:
            if date in date_unavailable_list:
                return HttpResponse('您预约的时间有人占用.\n占用时间包括:'+str(date_unavailable_list), status=200)
        print("this is post", data)
        if equip_item.waiting_list.filter(user_id=user_id):  # 判断是否申请过
            return HttpResponse('You already have a reservation for this equipment.', status=200)
        start_time = str(start_time[0]) + '/' + str(start_time[1]) + '/' + str(start_time[2])
        start_time = datetime.datetime.strptime(start_time, "%Y/%m/%d")
        end_time = str(end_time[0]) + '/' + str(end_time[1]) + '/' + str(end_time[2])
        end_time = datetime.datetime.strptime(end_time, "%Y/%m/%d")
        print('to here')
        #wl_item = LIST(user_id=user_id, user_name="who",rent_start=start_time, rent_exp=end_time,reason="1#2#4",apply_succes=False)
        data={"user_id":user_id, "user_name":user_name ,"rent_start":start_time,"rent_exp":end_time,"reason":reason,"apply_succes":False}
        print("this is data",data)
        serializer = WaitingSerializer(data=data)
        print('fuck')
        if serializer.is_valid():
            print('to here fianl')
            id=serializer.save()
            print( id.id,"this is motha id")

            query_set = LIST.objects.all()
            print('a',len(query_set))
            serializer =WaitingSerializer(query_set, many=True)
            print('ddd',serializer.data)
            obj=LIST.objects.get(id=id.id)
            print(obj)
            equip_item.waiting_list.add(obj)
            print('to here ADD SUCCESS',obj)


        return JsonResponse({"sucess":serializer.data})


@csrf_exempt
def cancel_waitlist(request):
    if request.method == 'POST':
        try:
            data = JSONParser().parse(request)
            equip_item = Equip.objects.get(id=data['equipid'])
            reservations = equip_item.waiting_list.all()

            for reservation in reservations:
                print('??')
                serial = WaitingSerializer(reservation)
                print('ak')
                print(serial.data)
                if(serial.data['user_id']==data['user_id']):
                    print(' == ')
                    obj = LIST.objects.get(id=serial.data['id'])
                    print(obj)
                    equip_item.waiting_list.remove(obj)  # ADD
                    print('delete success')
        except LIST.DoesNotExist:
            return HttpResponse("The waiting record you want to delete does not exist.", status=200)
        return HttpResponse("Quit from waiting list successfully.", status=200)


    return JsonResponse({}, status=400)

@csrf_exempt
def super_view_apply_equip_info(request):

    if request.method == 'POST':
        data = JSONParser().parse(request)
        if (check_password('0000', data['token'])):
            obj = Equip.objects.get(id=data['equipid'])
            serializer = EquipDesSerializer(obj)
            print(serializer.data)

            return JsonResponse(serializer.data, status=200)

        else:
            return HttpResponse({"error":"you are not super user"}, status=500)


@csrf_exempt
def super_view_equip_data_analyze(request):

    if request.method == 'GET':
        query_set = LIST.objects.all()
        serializers = WaitingSerializer(query_set, many=True)
        for reservation in serializers:
            print('a')
        # print(reservation.id,reservation.na)

        return JsonResponse({"list":"D"}, status=200)

    if request.method == 'POST':
        data = JSONParser().parse(request)
        if (check_password('0000', data['token'])):
            query_set = Equip.objects.all()
            serializer = EquipStatusSerializer(query_set, many=True)
            print(serializer.data)
            temp = sorted(serializer.data, key=lambda t: t['is_apply'], reverse=True)
            return JsonResponse({"list": list(json.loads(json.dumps(temp)))}, status=200)

        else:
            return HttpResponse({"error": "you are not super user"}, status=500)

