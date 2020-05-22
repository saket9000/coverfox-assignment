import uuid
from datetime import datetime, timedelta

from django.http import JsonResponse
from django.core import exceptions as django_exceptions
from django.utils import timezone

from keys.models import AvailableKeys, UsedKeys, AllKeys


# Create your views here.
def generate_key(request):
	"""
	Function to generate keys.
	"""

	# Generate UUID
	key = uuid.uuid1()
	try:
		# create a key
		AvailableKeys.objects.create(id=key)

		# Create a entry in All keys table to make sure that this key is purge after 5 minutes if keep
		# alive request is not received
		AllKeys.objects.create(key=key, valid_till=timezone.now() + timedelta(minutes=5))
		return JsonResponse({ 'message': 'Key generated successfully.', 'status': True })
	except Exception as e:
		return JsonResponse(
			{ 'message': 'Some error occured, please try again after some time.', 'status': False },
			status=500
		)

def get_available_key(request):
	"""
	Function to get available keys.
	"""
	try:
		# Return first available key
		key = AvailableKeys.objects.first()
		if not key:
			return JsonResponse(
				{ 'status': False, 'message': 'Key not found', 'key': None },
				status=404
			)
		_id = key.id

		# delete key from available table
		key.delete()

		# Make entry in used key table and add valid till for 60 seconds check if request is not received then
		# make this key available again
		key = UsedKeys.objects.create(id=_id, valid_till=timezone.now() + timedelta(seconds=60))
		return JsonResponse(
			{ 'status': True, 'message': 'Key allotted', 'key': key.id }
		)
	except Exception as e:
		return JsonResponse(
			{ 'message': 'Some error occured, please try again after some time.', 'status': False },
			status=500
		)

def unblock_key(request, key):
	"""
	Function to unblock key and make this available in E2 again.
	"""

	try:
		# Get used key
		key = UsedKeys.objects.get(id=key)
		_key = key.id

		# delete entry from used key and make this available again by creating enrty in AvailableKey table again
		key.delete()
		key = AvailableKeys.objects.create(id=_key)
		return JsonResponse(
			{ 'status': True, 'message': 'Key unblocked', 'key': key.id }
		)
	except django_exceptions.ObjectDoesNotExist as e:
		return JsonResponse(
			{ 'status': False, 'message': 'Key not found', 'key': None },
			status=404
		)
	except Exception as e:
		return JsonResponse(
			{ 'message': 'Some error occured, please try again after some time.', 'status': False },
			status=500
		)

def delete_key(request, key):
	"""
	Function to get purge key.
	"""

	try:
		# check if key exist or not
		used_keys = UsedKeys.objects.filter(id=key)
		available_keys = AvailableKeys.objects.filter(id=key)
		if not used_keys and not available_keys:
			return JsonResponse(
				{ 'status': False, 'message': 'Key not found' },
				status=404
			)

		# If keys are available then delete keys from all tables
		used_keys.delete()
		available_keys.delete()
		all_keys = AllKeys.objects.filter(key=key).delete()
		return JsonResponse({ 'status': True, 'message': 'Key purged successfully.' })
	except django_exceptions.ValidationError as e:
		return JsonResponse(
			{ 'status': False, 'message': 'Key not found' },
			status=404
		)
	except Exception as e:
		return JsonResponse(
			{ 'message': 'Some error occured, please try again after some time.', 'status': False },
			status=500
		)

def keep_key_alive(request, key):
	"""
	Function to keep key alive my 5 minutes.
	"""

	try:
		# search for key if available and still valid then increase it validty
		key = AllKeys.objects.get(key=key)
		key.valid_till = timezone.now() + timedelta(minutes=5)
		key.save()
		return JsonResponse({ 'status': True, 'message': 'Key kept alive request successful' })
	except django_exceptions.ObjectDoesNotExist as e:
		return JsonResponse(
			{ 'status': False, 'message': 'Key not found' },
			status=404
		)
	except Exception as e:
		return JsonResponse(
			{ 'message': 'Some error occured, please try again after some time.', 'status': False },
			status=500
		)
