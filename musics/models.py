# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Music(models.Model):
	song = models.TextField()
	singer = models.TextField()
	style = models.TextField()
	ceated = models.TextField()

	class Meta:
		db_table = "music"