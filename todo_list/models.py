from django.contrib.auth.models import User
from django.db.models import *
from django.db import models
import datetime

# Create your models here.
class Lists(models.Model):
    id=CharField(primary_key=True,max_length=30)
    name=CharField(max_length=30)
    date=DateTimeField(auto_created=True,default=datetime.datetime.now())
    color=CharField(max_length=40,default="skyblue")
    user=ForeignKey(User,on_delete=CASCADE)
    def __str__(self):
        return self.name

class Tasks(models.Model):
    belongsto_list=ForeignKey(Lists,on_delete=CASCADE)
    date=DateTimeField(auto_created=True,default=datetime.datetime.now())
    status=BooleanField(default=False)
    info=CharField(max_length=200)

    def __str__(self):
        return self.info