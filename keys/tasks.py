from __future__ import absolute_import
from celery import shared_task

from django.utils import timezone
from keys.models import AvailableKeys, UsedKeys, AllKeys


@shared_task
def release_blocked_keys():
	"""
	Function to release blocked key it runs every seconds and filter from valid time
	"""

	keys = UsedKeys.objects.filter(valid_till__lt=timezone.now())
	if keys:
		for key in keys:
			_key = key.id
			key.delete()
			AvailableKeys.objects.create(id=_key)

@shared_task
def delete_not_kept_alive_keys():
	"""
	Function to delete keys that are not kept alive
	"""

	keys = AllKeys.objects.filter(valid_till__lt=timezone.now())
	for key in keys:
		UsedKeys.objects.filter(id=key.key).delete()
		AvailableKeys.objects.filter(id=key.key).delete()
		key.delete()
