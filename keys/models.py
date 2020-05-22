import uuid
from django.db import models

# Create your models here.
class AvailableKeys(models.Model):
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	added_on = models.DateTimeField(auto_now_add=True, db_index=True)
	# updated_on = models.DateTimeField(auto_now=True, db_index=True)

	class Meta:
		db_table = 'available_keys'


class UsedKeys(models.Model):
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	valid_till = models.DateTimeField(db_index=True, null=True)

	class Meta:
		db_table = 'used_keys'


class AllKeys(models.Model):
	key = models.UUIDField(default=uuid.uuid4, editable=False, db_index=True)
	valid_till = models.DateTimeField(db_index=True, null=True)

	class Meta:
		db_table = 'all_keys'
