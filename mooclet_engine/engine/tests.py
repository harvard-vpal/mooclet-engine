from django.test import TestCase
# Create your tests here.

#temporary code to test contextual thompson sampling policy
class PolicyParams():
    parameters = {}

def test_thompson_sampling_contextual():
    dim = 3
    vars = None
    contexts = {}
    policy_params = PolicyParams()
    policy_params.parameters['regression_formula'] = 'y ~ x0 + x1'
    policy_params.parameters['action_space'] = {'matching': [0,1],'charity':[0,1,2]}
    policy_params.parameters['include_intercept'] = True

    policy_params.parameters['coef_mean'] = np.zeros(dim)
    policy_params.parameters['coef_cov'] = np.identity(dim)
    policy_params.parameters['variance_a'] = 2
    policy_params.parameters['variance_b'] = 2

    contexts['policy_parameters'] = policy_params

    #thompson_sampling_contextual(vars, contexts)

#test_thompson_sampling_contextual()