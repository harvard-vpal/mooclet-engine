from django.test import TestCase
import numpy as np
from scipy.stats import invgamma
from policies import thompson_sampling_contextual

# Create your tests here.
#temporary code to test contextual thompson sampling policy
class PolicyParams():
    parameters = {}

def test_thompson_sampling_contextual():
    dim = 6
    vars = None
    contexts = {}
    policy_params = PolicyParams()
    policy_params.parameters['regression_formula'] = 'y ~ x0 + x1 + matching_1 + matching_2 + charity'
    policy_params.parameters['action_space'] = {'matching_1': [0,1],'matching_2':[0,1],'charity':[0,1,2]}
    policy_params.parameters['include_intercept'] = True
    policy_params.parameters['contextual_variables'] = {'x0': 2.5,'x1':-0.7}

    policy_params.parameters['coef_mean'] = np.zeros(dim)
    policy_params.parameters['coef_cov'] = np.identity(dim)
    policy_params.parameters['variance_a'] = 2
    policy_params.parameters['variance_b'] = 2

    contexts['policy_parameters'] = policy_params

    thompson_sampling_contextual(vars, contexts)

test_thompson_sampling_contextual()
#calculate_outcome({'x0':2.5,'x1':-.75,'a0':1.2}, [5.0,-2.0,3.2,1.5,-1.0], True,'y ~ x0 + x1 + a0 + a0 * x1')
#print(is_valid_action({'matching_1':0,'char':3,'matching_0':1,'matching_2':0,'a_0':2,'a_2':0}))