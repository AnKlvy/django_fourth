# schema.py
import graphene
from graphene_django.types import DjangoObjectType
from .models import Task

class TaskType(DjangoObjectType):
    class Meta:
        model = Task

class Query(graphene.ObjectType):
    all_tasks = graphene.List(TaskType)
    task = graphene.Field(TaskType, id=graphene.Int())

    def resolve_all_tasks(root, info):
        return Task.objects.all()

    def resolve_task(root, info, id):
        return Task.objects.get(pk=id)

class CreateTask(graphene.Mutation):
    class Arguments:
        title = graphene.String(required=True)
        description = graphene.String(required=True)
        deadline_date = graphene.Date(required=True)
        status = graphene.Int(required=True)

    task = graphene.Field(TaskType)

    def mutate(self, info, title, description, deadline_date, status):
        task = Task(title=title, description=description, deadline_date=deadline_date, status=status)
        task.save()
        return CreateTask(task=task)

class UpdateTask(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)
        title = graphene.String()
        description = graphene.String()
        deadline_date = graphene.Date()
        status = graphene.Int()

    task = graphene.Field(TaskType)

    def mutate(self, info, id, title=None, description=None, deadline_date=None, status=None):
        task = Task.objects.get(pk=id)
        if title:
            task.title = title
        if description:
            task.description = description
        if deadline_date:
            task.deadline_date = deadline_date
        if status is not None:
            task.status = status
        task.save()
        return UpdateTask(task=task)

class DeleteTask(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)

    success = graphene.Boolean()

    def mutate(self, info, id):
        task = Task.objects.get(pk=id)
        task.delete()
        return DeleteTask(success=True)

class Mutation(graphene.ObjectType):
    create_task = CreateTask.Field()
    update_task = UpdateTask.Field()
    delete_task = DeleteTask.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)
