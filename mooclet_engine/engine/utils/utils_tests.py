import numpy as np
import pandas as pd
import utils

def test_create_design_matrix():
    #np.random.seed(1717)
    df = pd.DataFrame(np.random.randint(1, 5, (30, 3)), columns=['x0', 'x1', 'x2'])
    formula = "y ~ x1 + x2 + x0 * x1 + x1 * x2 + x0 * x1 * x2"
    print(df.head())
    print('formula: ' + formula)
    D = utils.create_design_matrix(df, formula, add_intercept=True)
    print(D.head())

test_create_design_matrix()

class PolicyParams():
    parameters = {}

def test_get_values():

    #variables = ['explanation', 'repdem']
    policy_params = PolicyParams()
    policy_params.parameters = {
                    "action_space": {"matching": [0,1],
                                "charity2": [0,1], 
                                "charity3":[0,1]},
                    "contextual_variables": ['repdem', 'version'],
                    "outcome_variable": "score"


                    }
    df = utils.values_to_df(16, policy_params)
    print(df.head())
test_get_values()