import logging
from functools import wraps

import requests
from django.conf import settings
from django.db import models
from django.db.models import Q

from .models import Webhook, WebhookAction


def run_webhook(webhook, action, payload=None):
    data = {
        'action': action,
    }
    if webhook.send_payload and payload:
        data.update(payload)
    try:
        return requests.post(
            webhook.url,
            headers=webhook.headers,
            json=data,
            timeout=settings.WEBHOOK_TIMEOUT,
        )
    except requests.RequestException as exc:
        logging.error(exc, exc_info=True)
        return


def emit_event(organization, action, instanses=None):
    webhooks = Webhook.objects.filter(
        Q(organization=organization) &
        Q(is_active=True) &
        (
            Q(send_for_all_actions=True) |
            Q(id__in=WebhookAction.objects.filter(
                webhook__organization=organization,
                action=action
            ).values_list('webhook_id', flat=True))
        )
    )
    if not webhooks.exists():
        return
    payload = None
    if instanses and webhooks.filter(send_payload=True).exists():
        serializer_class = WebhookAction.ACTIONS[action].get('serializer')
        if serializer_class:
            data = serializer_class(instance=instanses, many=True).data
            payload = {WebhookAction.ACTIONS[action]['key']: data}
    for wh in webhooks:
        run_webhook(wh, action, payload)


def api_webhook(action):
    def decorator(func):
        @wraps(func)
        def wrap(self, request, *args, **kwargs):
            responce = func(self, request, *args, **kwargs)
            emit_event(
                request.user.active_organization,
                action,
                [WebhookAction.ACTIONS[action]['model'].objects.get(id=responce.data.get('id'))]
            )
            return responce
        return wrap
    return decorator


def api_delete_webhook(action):
    def decorator(func):
        @wraps(func)
        def wrap(self, request, *args, **kwargs):
            obj = {'id': self.get_object().pk}
            responce = func(self, request, *args, **kwargs)
            emit_event(
                request.user.active_organization,
                action,
                [obj]
            )
            return responce
        return wrap
    return decorator
