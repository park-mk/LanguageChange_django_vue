from .models import Equip, LIST
from .serializers import EquipSerializer,EquipStatusSerializer,EquipONSerializer,EquipDesSerializer,EquipRentSerializer,EquipRentUserSerializer
from rest_framework.parsers import JSONParser
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import make_password,check_password
import json

from django.db.models.functions import (
    ExtractDay, ExtractMonth, ExtractYear
)
from .utils import add_print_date
import datetime
# Create your views here.

@csrf_exempt
def equip_list(request):
    if request.method == 'POST':


        print('superuser come to check users lists')
        if True:#(check_password('0000', request.body.decode("utf-8"))):
            query_set = Equip.objects.all()
            serializer =EquipStatusSerializer(query_set, many=True)
            print(serializer.data)
            temp = sorted(serializer.data, key=lambda t: t['is_apply'], reverse=True)

            return JsonResponse({"list":list(json.loads(json.dumps(temp)))}, status=200)
        else:
            return HttpResponse({"error": "you are not super user"}, status=500)

    elif request.method == 'PUT':
        print('to here')
        data = JSONParser().parse(request)
        serializer = EquipSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)


@csrf_exempt
def equip_on_list(request):
    if request.method == 'GET':

        print('user come to check users lists')
        if True:  # (check_password('0000', request.body.decode("utf-8"))):
            query_set = Equip.objects.all()
            print(query_set)
            serializer = EquipONSerializer(query_set, many=True)
            print(query_set)
            new2_list = [dd for dd in serializer.data if dd['is_on'] is True]
            new_list = new2_list
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

        if True :#(check_password('0000', data['token'])):



            try:
                obj = Equip.objects.get(id=data['equipid'])
            except:
                return JsonResponse({'status': 'false', 'message': "no such user"}, status=500)


            serializer = EquipRentUserSerializer(obj)

            return JsonResponse(serializer.data, status=201)




@csrf_exempt
def equip(request,id):
    #print(id)
    print('fuck')
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
        EquipStatusSerializer().deny_apply(record)
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








def user_to_waitinglist(request):
    #李同学请看，在这个函数你会收到三个参数1，设备id，2用户名，3用户id 将其一次排入waitinglist 中 并保证申请过的id无法在申请
    #最好也能实现一下 waitinglist的删除
    """
    :param request: POST
    :param equip_id: 借用设备ID
    :param user_id: 借用者ID
    :param time: 借用时间（整数），可以是小时，DELETE请求中可以没有
    :return:
    """
    equip_id = request.POST.get('equip_id').strip()
    user_id = request.POST.get('user_id').strip()
    start_time = request.POST.get('start').strip()
    end_time = request.POST.get('end').strip()

    try:
        equip = Equip.objects.get(id=equip_id)
    except Equip.DoesNotExist:
        return HttpResponse("The equip you want to operate does not exist.", status=200)

    date_unavailable_list = []      # 已占用的日期列表：形式['2020/7/8', '2020/7/9', ]
    reservations = equip.waiting_list.all()
    for reservation in reservations:
        rent_inf = reservation.objects.annotate(
            year_from=ExtractYear('rent_start'),
            month_from=ExtractMonth('rent_start'),
            day_from=ExtractDay('rent_start'),
            year_to=ExtractDay('rent_exp'),
            month_to=ExtractDay('rent_exp'),
            day_to=ExtractDay('rent_exp')
        ).get()
        add_print_date(year_from=rent_inf.year_from,
                       month_from=rent_inf.month_from,
                       day_from=rent_inf.day_from,
                       year_to=rent_inf.year_to,
                       month_to=rent_inf.month_to,
                       day_to=rent_inf.day_to,
                       list_of_date=date_unavailable_list)

    if request.method == 'GET':          # 检查今天是否在waitinglist预约时间内
        now_time = datetime.datetime.now()
        time_str = str(now_time.year) + '/' + str(now_time.month) + '/' + str(now_time.day)
        if time_str in date_unavailable_list:
            return HttpResponse('There is reservation today.', status=200)
        else:
            return HttpResponse('There is not reservation today.', status=200)

    if request.method == 'POST':
        start_time = request.POST.get('start').strip()  # 格式: '2020/7/8'
        end_time = request.POST.get('end').strip()

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

        for date in time_list:
            if date in date_unavailable_list:
                return HttpResponse('您预约的时间有人占用.\n占用时间包括:'+str(date_unavailable_list), status=200)

        if equip.waiting_list.filter(user_id=user_id):  # 判断是否申请过
            return HttpResponse('You already have a reservation for this equipment.', status=200)
        wl_item = LIST(user_id=user_id, rent_start=start_time, rent_exp=end_time)
        equip.waiting_list.add(wl_item)
        return HttpResponse("You have got in the waiting list successfully.", status=200)

    if request.method == 'DELETE':
        try:
            wl_item = equip.waiting_list.get(user_id=user_id, equip_id=equip_id)
        except LIST.DoesNotExist:
            return HttpResponse("The waiting record you want to delete does not exist.", status=200)
        wl_item.delete()
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


