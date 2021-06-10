from .models import Webhook
from functools import wraps


def api_webhook(action, payload_key):
    def decorator(func):
        @wraps(func)
        def wrap(self, request, *args, **kwargs):
            responce = func(self, request, *args, **kwargs)
            Webhook.emit_event(
                request.user.active_organization,
                action,
                payload={payload_key: responce.data},
            )
            return responce
        return wrap
    return decorator


def api_delete_webhook(action, payload_key):
    def decorator(func):
        @wraps(func)
        def wrap(self, request, *args, **kwargs):
            obj_id = self.get_object().pk
            responce = func(self, request, *args, **kwargs)
            Webhook.emit_event(
                request.user.active_organization,
                action,
                payload={payload_key: obj_id},
            )
            return responce
        return wrap
    return decorator
