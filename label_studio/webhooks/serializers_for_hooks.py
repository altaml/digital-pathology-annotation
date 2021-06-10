from rest_framework import serializers

from projects.models import Project
from tasks.models import Task, Annotation
# SERIALIZERS FOR WEBHOOKS


class OnlyIDWebhookSerializer(serializers.Serializer):
    id = serializers.IntegerField()

    class Meta:
        fields: ('id',)


class ProjectWebhookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'


class TaskWebhookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'


class AnnotationWebhookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Annotation
        fields = '__all__'
