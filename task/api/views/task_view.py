import datetime

from rest_framework import generics, status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from base.task_celery import send_email
from task.models import Task
from task.api.serializers import (
    GetTaskSerializer,
    TaskSerializer, DetailTaskSerializer
)


class CreateTaskView(generics.CreateAPIView):
    serializer_class = TaskSerializer


create = CreateTaskView.as_view()


class ListTaskView(generics.ListAPIView):
    serializer_class = GetTaskSerializer
    queryset = Task.objects.all()

    def get_queryset(self):
        return self.queryset.filter(
            owner=self.request.user
        )


list = ListTaskView.as_view()


class DetailTaskView(generics.RetrieveUpdateAPIView):
    serializer_class = DetailTaskSerializer
    queryset = Task.objects.all()
    lookup_field = 'id'

    def get_queryset(self):
        return self.queryset.filter(
            owner=self.request.user,
            id=self.kwargs['id']
        )


detail = DetailTaskView.as_view()


class DeleteTaskView(APIView):
    def delete(self, request, *args, **kwargs):
        task = get_object_or_404(Task, id=self.kwargs['id'])
        if task:
            task.delete()
            return Response(
                {"delete": "Успешно удалено"},
                status=status.HTTP_200_OK
            )
        return Response(
            {"detail": "Задача с таким ID не сущевствует"}
        )


delete = DeleteTaskView.as_view()


class ExecuteView(APIView):
    querset = Task.objects.all()
    def post(self, request, *args, **kwargs):
        task = get_object_or_404(Task, id=self.kwargs['id'])
        task.is_done = self.request.data.get("is_done", False)
        task.execution_time = datetime.datetime.now()
        task.save()
        user = self.request.user
        send_email.delay(user.id)
        return Response(
            {"result": "Статус успешно изменено"},
            status=status.HTTP_200_OK
        )
    def get_queryset(self):
        return self.querset.filter(
            id=self.kwargs['id']
        )

execute = ExecuteView.as_view()
