

from django.db import models


class SubjectLineMooclet(models.Model):
	'''
	subject line mooclet
	'''
	mooclet_id = models.PositiveIntegerField()

	def get_version(self):
		pass


class SubjectLine(models.Model):
	'''
	subject line version
	'''	
	version_id = models.PositiveIntegerField()
	text = models.CharField(max_length=200)



