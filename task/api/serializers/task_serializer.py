from task.models import Task
from rest_framework import serializers


class GetTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = (
            "id",
            "title",
            "is_done",
            "execution_time",
        )


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = (
            "id",
            "owner",
            "title",
            "description",
            "execution_time",
        )


class DetailTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = (
            "__all__"
        )