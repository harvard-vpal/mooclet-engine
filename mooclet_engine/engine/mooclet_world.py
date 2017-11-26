# -*- coding: utf-8 -*-
"""

@author: Imanol
"""

from email_mab.agents import *
from django.core.urlresolvers import reverse
from django.apps import apps
# from django.contrib.contenttypes.models import ContentType
from django.db.models import Avg
import json
import numpy as np
import numpy_indexed as npi
from numpy.random import choice, beta
import pandas as pd
import sys
import itertools
import os




def contextual_mab_policy(variables, context):


  versions = context['mooclet'].version_set.all()
  Agent_types = variables.get(name='agent_type')
  agent_types = Agent_types.get_data(context)

  agent_type = choice(agent_types).text

  world = World(variables, context)

  Variables = apps.get_model('engine','Variable')
  Values = apps.get_model('engine', 'Value')
  Users = apps.get_model('engine','Learner')
  context_Variables = Variables.objects.filter(name__in=world.context_variables)
  arm_Variables = Variables.objects.filter(name__in=world.arm_variables)
  # TODO redo for continous variables
  context_dict = {var.name:[val.value for val in var.get_data().exclude(learner=context['learner'])] for var in context_Variables}
  context_df = pd.DataFrame(context_dict)



  context_df = pd.get_dummies(context_df[world.context_variables],columns = world.context_variables)

  missing_context_columns = list(set(world.context_feature_vectors_names).difference(set(context_df.columns)))
  for col in missing_context_columns:
    context_df[col] = 0
  context_df = context_df[world.context_feature_vectors_names]


  arm_dict = {var.name:[val.value for val in var.get_data().exclude(learner=context['learner'])] for var in arm_Variables}
  arm_df = pd.DataFrame(arm_dict)
  arm_df = pd.get_dummies(arm_df[world.arm_variables],columns = world.arm_variables)

  missing_arm_columns = list(set(world.arm_feature_vectors_names).difference(set(arm_df.columns)))
  for col in missing_arm_columns:
    arm_df[col] = 0
  arm_df = arm_df[world.arm_feature_vectors_names]




  # TODO Check horizon and degree with Maria

  #TODO Understand how to read and put togeather a np.array with all the context history. The variable information should be stored
  # on a json file with the first level being the type of variable (context,arm,reard), the second one being the name of
  # the variable, and third being the data type (categorical or float (ints should be either categorical or floats)) and
  # the possible values in case the variable is categorical.
  reward_history =   [var.value for var in Variables.objects.filter(name__in=world.response_variable)[0].get_data()]
  context_history = np.array(context_df)
  arm_id_history = npi.indices(world.arm_feature_vectors, np.array(arm_df), missing='mask').data
  batch_id = len(arm_id_history)+1


  agent = getattr(sys.modules[__name__], agent_type)(world = world, horizon = 3000, batch_size = 1,
                                                     degree = 1,warm_up_context_history = context_history,
                                                     warm_up_arm_history = arm_id_history,
                                                     warm_up_reward_history = reward_history)


  # TODO : Make all these steps into function
  user_context_dict = {var.name:[val.value for val in var.get_data().filter(learner=context['learner'])] for var in context_Variables}
  user_context_df = pd.DataFrame(user_context_dict)


  user_context_df = pd.get_dummies(user_context_df[world.context_variables],columns = world.context_variables)

  missing_context_columns = list(set(world.context_feature_vectors_names).difference(set(user_context_df.columns)))
  for col in missing_context_columns:
    user_context_df[col] = 0
  user_context_df = user_context_df[world.context_feature_vectors_names]

  user_context = np.array(user_context_df)


  version_id =  agent.assign_arms_to_batch_of_contexts(user_context,batch_id)[0]

  version_names = world.get_arm_names(version_id)



  for i, var_name in enumerate(world.arm_variables):
    condition_var = Variables.objects.get(name=var_name)
    learner_var = Values.objects.filter(learner=context['learner'],variable=condition_var)
    version_name = version_names[i]

    version = versions.filter(name=version_name)[0]



    # If the treatment value already exists then do nothing and return the version already chosen
    if len(learner_var)==0:

      condition = Values.objects.create(variable = condition_var, learner = context['learner'],
                                      mooclet=context['mooclet'], value=version_id,
                                      text=version_names[i],version=version)
      condition.save()
    else:
      version = learner_var[0].version


      #version = value.version
      #version="ERROR: Learner already assigned to a condition"


  return version



class World:
  def __init__(self,variables, context):

    # Mooclet info
    self.variables = variables
    self.context = context

    # variable information
    cwd = os.getcwd()
    with open(os.path.join(cwd,'engine/var_info.json'),'r') as fl:
      self.var_info = json.load(fl)



    self.arm_variables_object =  self.var_info['arm_variables']
    self.context_variables_object = self.var_info['context_variables']
    self.response_variable = [self.var_info['response_variables'][0]['name']]

    self.initialize_arms()
    self.initilize_contexts()



  # Interface methods of agents with the world.


  def arm_features(self, arm_id):
    return self.arm_feature_vectors[int(arm_id)]

  def get_arm_names(self,arm_id):


    return self.arm_names[int(arm_id)]

  def get_arm_values(self,arm_id):
    return self.arm_values[int(arm_id)]

  #TODO add case when variables are continous instead of categorical
  def initialize_arms(self):

    # Get arm, context and response name in the correct order:

    arm_ids = [var['id'] for var in self.arm_variables_object]
    self.arm_variables_object = list(zip( *sorted( zip(arm_ids, self.arm_variables_object)))[1])
    self.arm_variables = [var['name'] for var in self.arm_variables_object]

    self.arm_values = [arm['values'] for arm in self.arm_variables_object if arm['type']=='categorical']
    self.arm_values = list(itertools.product(*self.arm_values))

    self.arm_names = [arm['text'] for arm in self.arm_variables_object if arm['type']=='categorical']
    self.arm_names = list(itertools.product(*self.arm_names))

    df = pd.DataFrame(self.arm_values, columns = self.arm_variables)


    self.arm_feature_vectors = pd.get_dummies(df[self.arm_variables], columns = self.arm_variables).drop_duplicates()
    self.arm_feature_vectors_names = self.arm_feature_vectors.columns
    self.arm_feature_vectors = np.array(self.arm_feature_vectors)
    self.arm_feature_count = self.arm_feature_vectors.shape[1]
    self.arm_count = len(self.arm_values)


  def initilize_contexts(self):

    context_ids = [var['id'] for var in self.context_variables_object]
    self.context_variables = [var['name'] for var in self.context_variables_object]
    self.context_variables = list(zip( *sorted( zip(context_ids, self.context_variables) ) )[1])

    self.context_names = [arm['values'] for arm in self.context_variables_object]
    self.context_names = list(itertools.product(*self.context_names))

    df = pd.DataFrame(self.context_names, columns = self.context_variables)


    self.context_feature_vectors = pd.get_dummies(df[self.context_variables],
                                                  columns = self.context_variables).drop_duplicates()
    self.context_feature_vectors_names = self.context_feature_vectors.columns
    self.context_feature_vectors = np.array(self.context_feature_vectors)
    self.context_feature_count = self.context_feature_vectors.shape[1]
    self.context_count = len(self.context_names)
    self.context_feature_vector_to_index = dict(zip(map(tuple, self.context_feature_vectors), range(0, self.context_count)))
