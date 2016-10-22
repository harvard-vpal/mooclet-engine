from __future__ import unicode_literals
import mooclet_api

from django.db import models

# override create method for TextMooclet
class TextMoocletManager(models.Manager):
	def create(self, *args, **kwargs):
		if 'mooclet_id' not in kwargs:
			kwargs['mooclet_id'] = mooclet_api.Mooclet.create(name=kwargs['text'])['id']
		return super(TextMoocletManager, self).create(*args, **kwargs)

class TextMooclet(models.Model):
	'''
	mooclet where versions have some text associated with them
	'''
	mooclet_id = models.PositiveIntegerField(blank=True)
	text = models.CharField(max_length=200)

	def get_version(self):
		mooclet_api.Mooclet.get_version()

# override create method for TextVersion
class TextVersionManager(models.Manager):
	def create(self, *args, **kwargs):
		if 'version_id' not in kwargs:
			kwargs['version_id'] = mooclet_api.Mooclet.create()['id']
		return super(TextVersionManager, self).create(*args, **kwargs)

class TextVersion(models.Model):
	'''
	generic mooclet version that contains text
	'''	
	version_id = models.PositiveIntegerField()
	text = models.CharField(max_length=200)
