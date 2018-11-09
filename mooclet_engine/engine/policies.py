from numpy.random import choice, beta
from django.core.urlresolvers import reverse
from django.apps import apps
# from django.contrib.contenttypes.models import ContentType
from django.db.models import Avg
import json
from collections import Counter
from .utils.utils import sample_no_replacement
from django.db.models.query_utils import Q

# arguments to policies:

# variables: list of variable objects, can be used to retrieve related data
# context: dict passed from view, contains current user, course, quiz, question context


def uniform_random(variables,context):
	return choice(context['mooclet'].version_set.all())

def weighted_random(variables,context):
	Weight = variables.get(name='version_weight')
	weight_data = Weight.get_data(context)

	versions = [weight.version for weight in weight_data]
	weights = [weight.value for weight in weight_data]
	return choice(versions, p=weights)

def thompson_sampling_placeholder(variables,context):
	return choice(context['mooclet'].version_set.all())

def thompson_sampling(variables,context):
	versions = context['mooclet'].version_set.all()
	#import models individually to avoid circular dependency
	Variable = apps.get_model('engine', 'Variable')
	Value = apps.get_model('engine', 'Value')
	Version = apps.get_model('engine', 'Version')
	# version_content_type = ContentType.objects.get_for_model(Version)
	#priors we set by hand - will use instructor rating and confidence in future
	prior_success = 19
	prior_failure = 1
	#max value of version rating, from qualtrics
	max_rating = 10

	version_to_show = None
	max_beta = 0

	for version in versions:
		student_ratings = Variable.objects.get(name='student_rating').get_data({'version': version}).all()
		rating_count = student_ratings.count()
		rating_average = student_ratings.aggregate(Avg('value'))
		rating_average = rating_average['value__avg']
		if rating_average is None:
			rating_average = 0


		#get instructor conf and use for priors later
		#add priors to db
		# prior_success_db, created = Variable.objects.get_or_create(name='thompson_prior_success')
		# prior_success_db_value = Value.objects.filter(variable=prior_success_db, version=version).last()
		# if prior_success_db_value:
		# 	#there is already a value, so update it
		# 	prior_success_db_value.value = prior_success
		# 	prior_success_db_value.save()
		# else:
		# 	#no db value
		# 	prior_success_db_value = Value.objects.create(variable=prior_success_db, version=version, value=prior_success)

		# prior_failure_db, created = Variable.objects.get_or_create(name='thompson_prior_failure')
		# prior_failure_db_value = Value.objects.filter(variable=prior_failure_db, version=version).last()
		# if prior_failure_db_value:
		# 	#there is already a value, so update it
		# 	prior_failure_db_value.value = prior_failure
		# 	prior_failure_db_value.save()
		# else:
		# 	#no db value
		# 	prior_failure_db_value = Value.objects.create(variable=prior_failure_db, version=version, value=prior_failure)
	

		#TODO - log to db later?
		successes = (rating_average * rating_count) + prior_success
		failures = (max_rating * rating_count) - (rating_average * rating_count) + prior_failure

		version_beta = beta(successes, failures)

		if version_beta > max_beta:
			max_beta = version_beta
			version_to_show = version

	return version_to_show


def sample_without_replacement(variables, context):
	mooclet = context['mooclet']
	policy_parameters = context['policy_parameters']
	# print "parameters:"
	# print policy_parameters
	conditions = None
	#print "starting"
	previous_versions = None

	Variable = apps.get_model('engine', 'Variable')
	Value = apps.get_model('engine', 'Value')
	Version = apps.get_model('engine', 'Version')

	if policy_parameters:
		# print "Has policy parameters"
		policy_parameters = policy_parameters.parameters

		if policy_parameters["type"] == "per-user" and context["learner"]:
			# print "Per user and Has learner"
			previous_versions = Version.objects.filter(value__variable__name="version", value__learner=context["learner"], mooclet=mooclet).all()
			# previous_versions = Value.objects.filter(learner=context['learner'], mooclet=mooclet, 
			# 					variable__name="version").values_list("version", flat=True)

		if 'variables' in policy_parameters and previous_versions:
			# print "previous versions " + str(len(previous_versions))
			variables = policy_parameters['variables']
			values = Value.objects.filter(version__in=previous_versions, variable__name__in=variables.keys()).select_related('variable','version').all()
			value_list = []
			for version in previous_versions:
				# print list(values.filter(version=version).all().values())
				value_list = value_list + list(values.filter(version=version).all().values("text","variable__name"))
			# print value_list
			conditions = {}
			for variable in variables.keys():
				#var_values = value_list.filter(variable__name=variable).values_list("text", flat=True)
				var_values = list(filter(lambda x: x["variable__name"] == variable, value_list)) 
				var_values = list(map(lambda x: x["text"], var_values)) 

				conditions[variable] = sample_no_replacement(variables[variable], var_values)


		elif 'variables' in policy_parameters:
			# print "variables but no user or prior context"
			#user hasn't seen versions previously
			variables = policy_parameters['variables']
			conditions = {}
			for variable in variables.iteritems():
				conditions[variable[0]] = choice(variable[1])


		# elif policy_parameters["type"] == "per-user" and context["learner"] and 'variables' not in policy_parameters:
		# 	if previous_versions:
		# 		version = sample_no_replacement(mooclet.version_set.all(), previous_versions)
		# 	else:
		# 		version = choice(context['mooclet'].version_set.all())

		if conditions:
			# print "conditions"
			# print conditions
			all_versions = mooclet.version_set.all()
			correct_versions = all_versions

			for condition in conditions:
				correct_versions = correct_versions.all().filter(Q(value__variable__name=condition, value__text=conditions[condition]))

			# print("All versions len:"+str(len(correct_versions.all())))
			version = correct_versions.first()



		else:
			#no version features, do random w/o replace within the versions
			# print "nothing"
			all_versions = mooclet.version_set.all()#values_list("version", flat=True)
			if not previous_versions:
				print "no prev vers"
				previous_versions = Version.objects.filter(value__variable__name="version", mooclet=mooclet).all()
			if previous_versions:
				version = sample_no_replacement(all_versions, previous_versions)
			else:
				version = choice(all_versions)


	else:
		#no version features, do random w/o replace within the versions
		# print "nothing"
		all_versions = mooclet.version_set.all()#values_list("version", flat=True)
		if not previous_versions:
			previous_versions = Version.objects.filter(value__variable__name="version", mooclet=mooclet).all()#Value.objects.filter(mooclet=mooclet, variable__name="version").values_list("version", flat=True)
		if previous_versions:
			version = sample_no_replacement(all_versions, previous_versions)
		else:
			version = choice(all_versions)

	return version




def sample_without_replacement2(variables, context):
	mooclet = context['mooclet']
	policy_parameters = context['policy_parameters']
	print "parameters:"
	print policy_parameters
	conditions = None
	print "starting"
	previous_versions = None
	version = None

	Variable = apps.get_model('engine', 'Variable')
	Value = apps.get_model('engine', 'Value')
	Version = apps.get_model('engine', 'Version')

	if policy_parameters:
		print "Has policy parameters"
		policy_parameters = policy_parameters.parameters

		if policy_parameters["type"] == "per-user" and context["learner"]:
			print "Per user and Has learner"
			#ALL versions
			previous_versions = Version.objects.filter(value__variable__name="version", mooclet=mooclet).all()

			previous_versions_user = previous_versions.filter(value__learner=context["learner"])

			if bool(previous_versions_user):
				print "has_previous_versions"
				#if previous versions, return a new set of factors
				all_versions = mooclet.version_set.all()
				factor_names = policy_parameters["variables"].keys()
				previous_version_factors = Value.objects.filter(variable__name__in=factor_names, version__in=previous_versions_user)

				new_factors = all_versions.exclude(value__variable__name__in=factor_names, value__text__in=previous_version_factors.values_list('text',flat=True)).all()
				version = choice(new_factors)
				#pass

			elif bool(previous_versions):
				min_seen_version = None
				min_seen_count = 0
				#no previous versions for the given user
				for version in previous_versions:
					count = Value.objects.filter(variable__name="version", version=version).count()
					if min_seen_version is None:
						min_seen_version = version
						min_seen_count = count
					elif count < min_seen_count:
						min_seen_version = version
						min_seen_count = count
				version = min_seen_version

			else:
				all_versions = mooclet.version_set.all()
				version = choice(all_versions)
				





	return version

