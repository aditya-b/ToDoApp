from django.http import JsonResponse
from django.utils.datastructures import MultiValueDictKeyError
from rest_framework.decorators import api_view
from rest_framework.status import *

from todo_list.models import Lists, Tasks
from todo_list.serializers import ListSerializer, TaskSerializer


#API to get all the lists and add a new list for a user
@api_view(['GET','POST'])
def list_api(request,user):
    if request.method == 'GET':
        lists=Lists.objects.filter(user__username=user)
        list_result=ListSerializer(lists,many=True)
        return JsonResponse(list_result.data,status=HTTP_200_OK)
    if request.method == 'POST':
        try:
            id=user+'_'+request.POST['name']
            list=Lists(name=request.POST['name'],id=id,colour=request.POST['colour'])
        except MultiValueDictKeyError:
            return JsonResponse({'error':"Error: Details do not match!"}, status=HTTP_409_CONFLICT)
        try:
            Lists.objects.get(id=id)
        except Exception:
            list.save()
            list_detail=ListSerializer(list)
            return JsonResponse(list_detail.data,status=HTTP_201_CREATED)
        return JsonResponse({'error':'List with same id exists!'},status=HTTP_409_CONFLICT)

#API to get, update, add tasks to a list and also delete the list
@api_view(['GET','POST','PUT','DELETE'])
def tasks_api(request,user,id):
    if request.method == 'GET':
        tasks=Tasks.objects.filter(belongsto_list__id=id,belongsto_list__user__username=user).order_by('-date')
        tasks_data=TaskSerializer(tasks,many=True)
        return JsonResponse(tasks_data.data, status=HTTP_200_OK)
    if request.method == 'POST':
        try:
            list=Lists.objects.get(id=id)
            if list.user.username != user:
                return JsonResponse({'error': 'No permissions!'}, status=HTTP_403_FORBIDDEN)
            try:
                info = request.POST['info']
                task = Tasks(info=info, belongsto_list=list)
                task.save()
            except MultiValueDictKeyError:
                return JsonResponse({'error': "Error: Details do not match!"}, status=HTTP_409_CONFLICT)
        except Exception:
            return JsonResponse({'error': 'List doesnt exist!'}, status=HTTP_404_NOT_FOUND)
    if request.method == 'PUT':
        tasks = Tasks.objects.filter(belongsto_list__id=id, belongsto_list__user__username=user).order_by('-date')
        i = 0
        for task in tasks:
            try:
                if request.POST[str(task.id)] == 'done':
                    task.status = True
            except Exception:
                task.status = False
            i += 1
            task.save()
        tasks=TaskSerializer(tasks,many=True)
        return JsonResponse(tasks.data, status=HTTP_200_OK)
    if request.method == 'DELETE':
        try:
            Lists.objects.get(id=id,user__username=user).delete()
            return JsonResponse({'message':'Delete successful!'},status=HTTP_200_OK)
        except Exception:
            return JsonResponse({'error': 'List not found'}, status=HTTP_404_NOT_FOUND)
