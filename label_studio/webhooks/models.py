from django.db import models
from django.utils.translation import gettext_lazy as _


class Webhook(models.Model):

    organization = models.ForeignKey('Webhook', on_delete=models.CASCADE, related_name='webhooks')

    url = models.URLField(_('URL of webhook'), max_length=2048)

    send_payload = models.BooleanField(_("does webhook send the payload"))

    class Meta:
        db_table = 'webhook'


class WebhookAction:
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

    webhook = models.ForeignKey('Webhook', on_delete=models.CASCADE, related_name='actions')

    action = models.CharField(_('action of webhook'), choices=ACTIONS, max_length=128, db_index=True,)

    class Meta:
        db_table = 'webhook_action'
        unique_together = [['webhook', 'action']]
