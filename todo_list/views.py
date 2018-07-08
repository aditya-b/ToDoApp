from django.contrib.auth.decorators import login_required
from django.shortcuts import loader
from django.http import HttpResponse, HttpResponseRedirect
from django.template.defaultfilters import register
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect

# Create your views here.
from django.views.generic.base import View

from todo_list.login_form import LoginForm
from .models import *


@register.filter(name='look')
def look(dict_val,arg):
    return dict_val[arg]

# Create your views here.
@login_required(login_url='todolist:login')
def lists(request):
    all_lists = list(Lists.objects.values().filter(user__username=request.user))
    list_copy = all_lists.copy()
    task_status = {}
    for l in list_copy:
        tasks = Tasks.objects.filter(belongsto_list__id=l['id'],belongsto_list__user__username=request.user)
        try:
            task_status[l['id']] = int(100 - ((tasks.filter(status=False).count() * 100) / (tasks.count())))
        except ZeroDivisionError:
            task_status[l['id']] = int(-1)
    template = loader.get_template('index.html')
    content = {
        'lists': all_lists,
        'tasks': task_status
    }
    return HttpResponse(template.render(content, request))

@login_required(login_url='todolist:login')
def get_tasks(request,list):
    all_tasks=Tasks.objects.filter(belongsto_list__id=list,belongsto_list__user__username=request.user).order_by('-date')
    color=Lists.objects.values('color','name').filter(id=list,user__username=request.user)
    name=''
    for c in color:
        name = c['name']
        color = c['color']
        break
    template=loader.get_template('tasks.html')
    content={
        'all_tasks' : all_tasks,
        'color':color,
        'name': name
    }
    return HttpResponse(template.render(content,request))

@login_required(login_url='todolist:login')
def add_list(request):
    template = loader.get_template('add_list.html')
    return HttpResponse(template.render(None,request))

@login_required(login_url='todolist:login')
def add_list_to_db(request):
    name=request.POST['name']
    color=request.POST['color']
    id = str(request.user) + '_' + name
    user=User.objects.get(username=request.user)
    list=Lists(id=id,name=name,color=color,user=user)
    list.save()
    return HttpResponseRedirect('/lists/')

@login_required(login_url='todolist:login')
def delete_list(request,list):
    Lists.objects.get(id=list,user__username=request.user).delete()
    return HttpResponseRedirect('/lists/')

@login_required(login_url='todolist:login')
def add_tasks(request,list):
    info=request.POST['info']
    l=Lists.objects.get(id=list,user__username=request.user)
    task=Tasks(info=info,belongsto_list=l)
    task.save()
    url='/lists/'+list+'/tasks/'
    return HttpResponseRedirect(url)

@login_required(login_url='todolist:login')
def edit_tasks(request,list):
   tasks=Tasks.objects.filter(belongsto_list__id=list,belongsto_list__user__username=request.user).order_by('-date')
   i=0
   for task in tasks:
       try:
           if request.POST[str(task.id)] == 'on':
               task.status=True
       except Exception:
           task.status=False
       i+=1
       task.save()
   url = '/lists/' + list + '/tasks/'
   return HttpResponseRedirect(url)

class LoginView(View):
    def get(self,request,*args,**kwargs):
        form = LoginForm()
        return render(request,'login.html',{'form':form,'message':None})

    def post(self,request,*args,**kwargs):
        form = LoginForm(request.POST)
        if form.is_valid():
            values = list(form.cleaned_data.values())
            user=authenticate(request,username=values[0],password=values[1])
            if user is not None:
                login(request,user)
                return redirect('todolist:lists')
            else:
                return render(request,'login.html',{'form':form,'message':'Invalid credentials!'})

def log_out(request):
    logout(request)
    return redirect('todolist:login')


