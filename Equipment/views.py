from .models import Equip, LIST
from .serializers import EquipSerializer,EquipStatusSerializer,EquipONSerializer,EquipDesSerializer,EquipRentSerializer,EquipRentUserSerializer
from rest_framework.parsers import JSONParser
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import make_password,check_password
import json
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

    try:
        equip = Equip.objects.get(id=equip_id)
    except Equip.DoesNotExist:
        return HttpResponse("The equip you want to operate does not exist.", status=200)

    if request.method == 'POST':
        time = int(request.POST.get('time').strip())
        if equip.waiting_list.filter(user_id=user_id, equip_id=equip_id):  # 判断是否申请过
            return HttpResponse('You already have a reservation for this equipment.', status=200)
        wl_item = LIST(user_id=user_id, equip_id=equip_id, time=time)
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


@csrf_exempt
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