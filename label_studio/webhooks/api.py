import logging

from drf_yasg.utils import swagger_auto_schema
from django.utils.decorators import method_decorator
from rest_framework import generics

from .models import Webhook
from .serializers import WebhookSerializer


@method_decorator(
    name='get',
    decorator=swagger_auto_schema(
        tags=['Webhooks'],
        operation_description="List of webhooks"
    )
)
@method_decorator(
    name='post',
    decorator=swagger_auto_schema(
        tags=['Webhooks'],
        operation_description="Create a webhooks"
    )
)
class WebhookListAPI(generics.ListCreateAPIView):
    queryset = Webhook.objects.all()
    serializer_class = WebhookSerializer

    def get_queryset(self):
        return Webhook.objects.filter(organization=self.request.user.active_organization)

    def perform_create(self, serializer):
        serializer.save(organization=self.request.user.active_organization)

    # permission_classes = [IsAdminUser]


@method_decorator(name='get', decorator=swagger_auto_schema(tags=['Webhooks'],))
@method_decorator(name='put', decorator=swagger_auto_schema(tags=['Webhooks'],))
@method_decorator(name='patch', decorator=swagger_auto_schema(tags=['Webhooks'],))
@method_decorator(name='delete', decorator=swagger_auto_schema(tags=['Webhooks'],))
class WebhookAPI(generics.RetrieveUpdateDestroyAPIView):
    queryset = Webhook.objects.all()
    serializer_class = WebhookSerializer

    def get_queryset(self):
        return Webhook.objects.filter(organization=self.request.user.active_organization)
