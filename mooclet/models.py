from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.shortcuts import redirect
# from django.contrib.contenttypes.models import ContentType
# from django.contrib.contenttypes.fields import GenericForeignKey
import policies


class Mooclet(models.Model):
    name = models.CharField(max_length=100,default='')

    policy = models.ForeignKey('Policy',blank=True,null=True)

    def __unicode__(self):
        return "Mooclet {}: {}".format(self.pk, self.name)

    def get_version(self, policy=None, context={}):
        context['versions'] = self.version_set.all()
        if not policy:
        	policy = self.policy
        version = policy.run_policy(context)

        return version


class Version(models.Model):
    '''
    Mooclet version
    '''
    mooclet = models.ForeignKey(Mooclet, null=True)
    name = models.CharField(max_length=200,default='')

    def __unicode__(self):
        return "Version {}: {}".format(self.pk, self.name)


class Policy(models.Model):
    name = models.CharField(max_length=100)
    # variables = models.ManyToManyField('Variable') # might use this for persistent "state variables"?

    class Meta:
        verbose_name_plural = 'policies'

    def __unicode__(self):
        return self.name

    def get_policy_function(self):
        try:
            return getattr(policies, self.name)
        except:
            print "policy function matching specified name not found"
            # TODO look through custom user-provided functions
            return None

    # def get_variables(self):
    #     # TODO implement returning all, subsets, etc.
    #     return self.variables.all()

    # def run_policy(self, context):
    #     # insert all version ids here?
    #     policy_function = self.get_policy_function()
    #     variables = self.get_variables()
    #     version_id = policy_function(variables,context)
    #     return version_id


# class MoocletPolicyState(models.Model):
# 	pass


# class Variable(models.Model):
#     name = models.CharField(max_length=100)
#     display_name = models.CharField(max_length=200,default='')
#     is_user_variable = models.BooleanField(default=False)
#     description = models.TextField(default='')


#     user = models.BooleanField()
#     mooclet = models.BooleanField()
    


#     def __unicode__(self):
#         return self.display_name or self.name

#     @property
#     def object_name(self):
#         return self.content_type.__unicode__()

#     def get_data(self,context=None):
#         '''
#         return relevant value objects for the variable type
#         '''
#         # context is a dictionary that contains model objects user, course, quiz, mooclet, version
#         if context:
#             related_object = self.object_name # str: 'course','user','mooclet', or 'version'

#             query = {}
#             # if user variable and user info in context, filter by user
#             if 'user' in context and self.is_user_variable:
#                 query['user'] = context['user']

#             # if context is at the mooclet-level but variable is version-related, pass related version ids to the query
#             if 'mooclet' in context and related_object=='version':
#                 query['object_id__in'] = context['mooclet'].version_set.values_list('id',flat=True)
#             else:
#                 query['object_id'] = context[related_object].id # pk of related content object instance
#             return self.value_set.filter(**query)
#         else:
#             return self.value_set.all()

#     def get_data_dicts(self,context=None):
#         '''
#         return relevant values for the variable type, as a list of dicts
#         '''
#         return self.get_data(context).values()


# class Value(models.Model):
#     '''
#     user variable observation, can be associated with either course, mooclet, or mooclet version
#     examples of user variables:
#         course-level: general student characteristics
#         quiz-level: number of attempts
#         mooclet: ?
#         version: student rating of an explanation, instructors prior judgement
#     '''
#     user = models.ForeignKey(User,null=True,blank=True)
#     variable = models.ForeignKey(Variable)
#     object_id = models.PositiveIntegerField(null=True) # This can just be the integer primary key of the table specified in Variable as content_type
#     value = models.FloatField()
#     timestamp = models.DateTimeField(null=True,auto_now=True)

#     def __unicode__(self):
#         var_name = self.variable.name if self.variable.name else ""
#         value = self.value if self.value else ""
#         var_content_type = self.variable.content_type.name if self.variable.content_type else ""
#         value_object_id = self.object_id if self.object_id else ""
#         return "{}={}, {}={}".format(var_name, value, var_content_type, value_object_id) 

#     def get_object_content(self,content_object_name):
#         '''
#         retrieve the related content object associated with the Value
#         takes as input the name of the content object
#         '''
#         ct = self.variable.content_type
#         if ct.__unicode__() != content_object_name:
#             return None
#         return ct.get_object_for_this_type(pk=self.object_id)

#     @property
#     def object_name(self):
#         return self.variable.content_type.__unicode__()

#     # enables use of "value.course", etc. syntax

#     @property
#     def mooclet(self):
#         return self.get_object_content('mooclet')

#     @property
#     def version(self):
#         return self.get_object_content('version')


