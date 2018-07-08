import click,sys,os,django

sys.path.append('F:/Mission RnD/todo/todo')
os.environ['DJANGO_SETTINGS_MODULE'] = 'onlinedb.settings'
django.setup()
from todo_list.models import *



@click.group()
def to_do_main():
    '''Application to manage your TO-DO list'''

@to_do_main.command()
def create_list():
    '''Used to create a new list'''
    name_of_list=input('Enter list name (must be unique): ')
    list_new=Lists(name=name_of_list)
    list_new.id=None
    try:
        list_new.save()
        print('List successfully added!')
    except Exception as e:
        print(e)

@to_do_main.command()
def show_lists():
    '''Used to view all the existing lists'''
    lists=Lists.objects.all()
    print('Name','Date created',sep='\t')
    for l in lists:
        print(l.name,l.date,sep="\t")

@to_do_main.command()
@click.argument('list_name',nargs=1,required=True)
def create_task(list_name):
    '''Used to create a task in a list'''
    try:
        l=Lists.objects.get(name=list_name)
    except Exception as e:
        print(e)
        return
    id=input("Give an identifier to your task: ")
    task=input("Enter the task information: ")
    new_task=Tasks(name=id,task=task,belongsto_list=l)
    try:
        new_task.save()
        print('Task successfully added!')
    except Exception as e:
        print(e)

@to_do_main.command()
@click.argument('list_name',nargs=1,required=True)
def view_tasks(list_name):
    '''Used to view the tasks in a list'''
    try:
        l=Lists.objects.get(name=list_name)
        print('Name','Date Created',sep="\t")
        for list_object in l:
            print(l.name,l.date,sep='\t')
    except Exception as e:
        print(e)
        return

@to_do_main.command()
@click.argument('list_name',nargs=1,required=True)
@click.argument('task_name',nargs=1,required=True)
def mark_task(list_name,task_name):
    '''Used to mark a task complete'''
    try:
        task=Tasks.objects.all().filter(belongsto_list__=list_name,name=task_name)
        task.status=True
        print('Task successfully marked!')
    except Exception as e:
        print(e)

@to_do_main.command()
@click.argument('list_name',nargs=1,required=True)
@click.argument('task_name',nargs=1,required=True)
def delete_task(list_name,task_name):
    try:
        Tasks.objects.all().filter(belongsto_list__=list_name,name=task_name).delete()
        print('Task successfully deleted!')
    except Exception as e:
        print(e)