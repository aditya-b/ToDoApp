from django.urls import path

from todo_list.views import *

app_name='todolist'

urlpatterns=[
    path('lists/', lists,name='lists'),
    path('lists/<str:list>/tasks/', get_tasks),
    path('lists/<str:list>/tasks/edit_task/', edit_tasks),
    path('lists/<str:list>/tasks/delete_list/', delete_list),
    path('lists/<str:list>/tasks/add/', add_tasks),
    path('lists/add/', add_list),
    path('lists/add/add_list', add_list_to_db),
    path('login/',LoginView.as_view(),name='login'),
    path('logout/',log_out,name='logout')
]