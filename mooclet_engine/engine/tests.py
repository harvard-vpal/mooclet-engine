from django.test import TestCase
import numpy as np
from scipy.stats import invgamma
from policies import thompson_sampling_contextual

# Create your tests here.
#temporary code to test contextual thompson sampling policy
class PolicyParams():
    parameters = {}

# Function used for testing the linear contextual bandit
def test_thompson_sampling_contextual():
    
    # Number of regression parameters
    dim = 6
    vars = None
    contexts = {}
    policy_params = PolicyParams()
    
    # Specify regression model
    # policy_params.parameters['regression_formula'] = 'y ~ x0 + x1 + matching_1 + matching_2 + charity'
    
    policy_params.parameters['regression_formula'] = 'y ~ Age + charity_2 + charity_3 + matching_2 + matching_3'

    # Specify action variables
    policy_params.parameters['action_space'] = {'charity_2': [0,1],'charity_3':[0,1],'matching_2':[0,1], 'matching_3':[0,1]}
    # Specify intercept
    policy_params.parameters['include_intercept'] = True
    # Specify context
    policy_params.parameters['contextual_variables'] = {'Age': 19}

    ## Specify normal-inverse-gamma parameters 
    # Mean of coefficients 
    policy_params.parameters['coef_mean'] = np.zeros(dim)
    # Covariance matrix of coefficients
    policy_params.parameters['coef_cov'] = np.identity(dim)
    # Shape and scale parameters
    policy_params.parameters['variance_a'] = 2
    policy_params.parameters['variance_b'] = 2

    # Store normal inverse gamma parameters
    contexts['policy_parameters'] = policy_params
    
    # Run thompson sampling function
    thompson_sampling_contextual(vars, contexts)

test_thompson_sampling_contextual()
#calculate_outcome({'x0':2.5,'x1':-.75,'a0':1.2}, [5.0,-2.0,3.2,1.5,-1.0], True,'y ~ x0 + x1 + a0 + a0 * x1')
#print(is_valid_action({'matching_1':0,'char':3,'matching_0':1,'matching_2':0,'a_0':2,'a_2':0}))


## Testing posterior draw function

# Fill data frame (1 to 5 randomly)
df = pd.DataFrame(np.random.randint(1,5,(samplesize,4)),columns = ['C2','C3','M', 'R'])

# String formula
formula = "y ~ C2 + C3 + M + R"

# Generate outcome randomly 1 to 5
outcome = np.random.randint(1,5,samplesize)

# Create design matrix
# Note: create_design_matrix in policies.py
D = create_design_matrix(df, formula, add_intercept=True)
design_multiple = np.column_stack((D["Intercept"], D["C2"], D["C3"], D["M"], D["R"]))

# Prior parameters (mean vector, covariance matrix, shape and scale)
# Note: regression parameter dim = 5 (constant, C2, C3, M, and R)
m_pre = np.zeros(5)
V_pre = np.identity(5)
a1_pre = 2
a2_pre = 2

# Posterior draw given data (y,X) and parameters (mean, cov, a, b) 
posteriors(outcome, design_multiple, m_pre, V_pre, a1_pre, a2_pre)

