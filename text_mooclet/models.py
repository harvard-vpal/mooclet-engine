from __future__ import unicode_literals
import mooclet_api

from django.db import models

# managers

# override create method for TextMooclet
class MoocletManager(models.Manager):
	def create(self, *args, **kwargs):
		if 'mooclet_id' not in kwargs:
			kwargs['mooclet_id'] = mooclet_api.Mooclet.create()['id']
		return super(TextMoocletManager, self).create(*args, **kwargs)

# override create method for TextVersion
class VersionManager(models.Manager):
	def create(self, *args, **kwargs):
		if 'version_id' not in kwargs:
			kwargs['version_id'] = mooclet_api.Version.create()['id']
		return super(TextVersionManager, self).create(*args, **kwargs)

# models

class TextMooclet(models.Model):
	'''
	mooclet where versions have some text associated with them
	'''
	mooclet_id = models.PositiveIntegerField(null=True,blank=True)
	text = models.CharField(max_length=200)
	objects = MoocletManager()

	def get_version(self):
		version = mooclet_api.Mooclet.get_version(pk=self.pk)
		return self.textversion_set.get(pk=version['id'])


class TextVersion(models.Model):
	'''
	generic mooclet version that contains text
	'''	
	version_id = models.PositiveIntegerField(null=True,blank=True)
	text_mooclet = models.ForeignKey(TextMooclet)
	text = models.TextField(default='')
	objects = VersionManager()
