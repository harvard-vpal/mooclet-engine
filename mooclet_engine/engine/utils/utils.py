from numpy.random import choice
from collections import Counter
import pandas as pd
import numpy as np
from django.apps import apps

def sample_no_replacement(full_set, previous_set=None):
	# print "starting sample_no_replacement"
	# if previous_set:
	# 	print "prev set"
	# 	print previous_set
	# print full_set

	if set(previous_set) == set(full_set):
		#the user has seen each of the conditions of this vairbales at least once
		cond_counts = Counter(previous_set)
		#return a list of tuples of most common e.g.
		#[('a', 5), ('r', 2), ('b', 2)]
		cond_common_order = cond_counts.most_common()
		# print "cond_common_order"
		# print cond_common_order
		if cond_common_order[0][1] == cond_common_order[-1][1]:
			#all conds are evenly assigned, choose randomly
			cond = cond_common_order[choice(len(cond_common_order))]
			#print cond
			cond = cond[0]
		else:
			#choose the one with least assignment 
			#(where same value is ordered arbitrarily)
			cond = cond_common_order[-1][0]
	else:
		#subject hasn't seen all versions yet
		cond_choices = set(full_set) - set(previous_set)
		# print "cond_choices"
		# print cond_choices
		cond = choice(list(cond_choices))

	return cond

def create_design_matrix(input_df, formula, add_intercept = True):
    '''
    :param input_df:
    :param formula: for eaxmple "y ~ x0 + x1 + x2 + x0 * x1 + x1 * x2"
    :param add_intercept: whether to add dummy columns of 1.
    :return: the design matrix as a dataframe, each row corresponds to a data point, and each column is a regressor in regression
    '''

    D_df = pd.DataFrame()
    input_df = input_df.astype(np.float64)

    # parse formula
    formula = formula.strip()
    all_vars_str = formula.split('~')[1].strip()
    dependent_var = formula.split('~')[0].strip()
    vars_list = all_vars_str.split('+')
    vars_list = list(map(str.strip, vars_list))

    ''''#sanity check to ensure each var used in
    for var in vars_list:
        if var not in input_df.columns:
            raise Exception('variable {} not in the input dataframe'.format((var)))'''

    # build design matrix
    for var in vars_list:
        if '*' in var:
            interacting_vars = var.split('*')
            interacting_vars = list(map(str.strip,interacting_vars))
            D_df[var] = input_df[interacting_vars[0]]
            for i in range(1, len(interacting_vars)):
                D_df[var] *= input_df[interacting_vars[i]]
        else:
            D_df[var] = input_df[var]

    # add dummy column for bias
    if add_intercept:
        D_df.insert(0, 'Intercept', 1.)

    return D_df


def values_to_df(mooclet, policyparams, latest_update=None):
    """
    where variables is a list of variable names
    note: as implemented this will left join on users which can result in NAs
    """
    Value = apps.get_model('engine', 'Value')
    variables = policyparams["contextual_variables"]
    outcome = policyparams["outcome_variable"]
    variables.append(outcome)
    if not latest_update:
        values = Value.objects.filter(variable__name__in=variables, mooclet=mooclet)
    else: 
        values = Value.objects.filter(variable__name__in=variables, mooclet=mooclet, timestamp__gte=latest_update)
    vals_to_df = []
    curr_user = None
    #TODO: if the variable is "version" get the mapping to actions
    for value in values:
        if curr_user is None:
            curr_user = value.learner.id
            curr_user_values = {'user_id': curr_user}
        if value.learner != curr_user:
            #append to df
            vals_to_df.append(pd.DataFrame.from_records(curr_user_values, index=[0]))
            curr_user = value.learner.id
            curr_user_values = {'user_id': curr_user}

        #transform mooclet version shown into dummified action
        if value.variable.name == 'version':
                action_config = policyparams['actions']
                #this is the numerical representation from the config
                for action in action_config:
                    curr_action_config = value.version.version_json[action]
                    curr_user_values[action] = curr_action_config

        else:
            curr_user_values[value.variable.name] = value.value
        print curr_user_values
        vals_to_df.append(pd.DataFrame.from_records(curr_user_values, index=[0]))

    output_df = pd.concat(vals_to_df)
    output_df = output_df.dropna()
    #print output_df.head()
    return output_df
