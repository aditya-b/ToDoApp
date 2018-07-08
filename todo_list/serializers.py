from rest_framework.fields import CharField, IntegerField
from rest_framework.serializers import Serializer, ModelSerializer

from todo_list.models import Tasks, Lists


class ListViewSerializer(Serializer):
    name=CharField()
    color=CharField()
    status=IntegerField()

    def create(self, validated_data):
        return ListViewSerializer.objects.create(**validated_data)

class TaskViewSerializer(ModelSerializer):
    class Meta:
        model = Tasks
        exclude=['belongsto_list']

    def __str__(self):
        return self.data

class TaskSerializer(ModelSerializer):
    class Meta:
        model=Tasks
        exclude=[]

    def __str__(self):
        return self.data

class ListSerializer(ModelSerializer):
    class Meta:
        model=Lists
        exclude=[]

    def __str__(self):
        return self.data