from core.validators import JSONSchemaValidator
from django.db import models
from django.utils.translation import gettext_lazy as _


HEADERS_SCHEMA = {
    "type": "object",
    "patternProperties": {
        "^[a-zA-Z0-9-_]+$": {"type": "string"},
    },
    "maxProperties": 10,
    "additionalProperties": False
}


class Webhook(models.Model):

    organization = models.ForeignKey('organizations.Organization', on_delete=models.CASCADE, related_name='webhooks')

    url = models.URLField(_('URL of webhook'), max_length=2048)

    send_payload = models.BooleanField(_("does webhook send the payload"), default=True)

    send_for_all_actions = models.BooleanField(_("Use webhook for all actions"), default=True)

    headers = models.JSONField(_("request extra headers of webhook"),
                               validators=[JSONSchemaValidator(HEADERS_SCHEMA)],
                               default=dict)

    is_active = models.BooleanField(_("Is webhook active"), default=True)

    def get_actions(self):
        return WebhookAction.objects.filter(webhook=self).values_list('action', flat=True)

    def set_actions(self, actions):
        if not actions:
            actions = set()
        actions = set(actions)
        old_actions = set(self.get_actions())

        for new_action in list(actions - old_actions):
            WebhookAction.objects.create(webhook=self, action=new_action)

        WebhookAction.objects.filter(webhook=self, action__in=(old_actions-actions)).delete()

    def has_permission(self, user):
        return self.organization.has_user(user)

    class Meta:
        db_table = 'webhook'


class WebhookAction(models.Model):
    PROJECT_CREATED = 'PROJECT_CREATED'
    PROJECT_PUBLISHED = 'PROJECT_PUBLISHED'
    PROJECT_FINISHED = 'PROJECT_FINISHED'
    ANNOTATION_CREATED = 'ANNOTATION_CREATED'
    ANNOTATION_UPDATED = 'ANNOTATION_UPDATED'
    TASKS_IMPORTED = 'TASKS_IMPORTED'

    ACTIONS = [
        [PROJECT_CREATED, _('Project created')],
        [PROJECT_PUBLISHED, _('Project published')],
        [PROJECT_FINISHED, _('Project finished')],
        [ANNOTATION_CREATED, _('Annotation created')],
        [ANNOTATION_UPDATED, _('Annotation updated')],
        [TASKS_IMPORTED, _('Tasks imported')],
    ]

    webhook = models.ForeignKey(Webhook, on_delete=models.CASCADE, related_name='actions')

    action = models.CharField(_('action of webhook'), choices=ACTIONS, max_length=128, db_index=True,)

    class Meta:
        db_table = 'webhook_action'
        unique_together = [['webhook', 'action']]
