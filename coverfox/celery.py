#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import absolute_import

import os

from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'coverfox.settings')

from django.conf import settings

app = Celery('coverfox')

app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
