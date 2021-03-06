"""
	Generate datasets with input data X and outputs Y.  The target
    	is generated with a uniform distribution in [-1, 1].  The
    	first 20 features are generated from the target adding
    	incremental white Gaussian noise.  The others are generated
    	summing some white Gausian noise to a uniform distribution
    	similar but independent from target .

	PARAMETERS:
	       samples    - Number of examples.
	       features   - Number of features.
	       impFeat    - The number of relevant features 
	       min_sigma  - The minimum variance of the white noise for relevant features
	       max_sigma  - The maximum variance for the relevant features
	       sigma_const- Variance of the white noise for independent features   		
					
	OUTPUTS:
		X         - The matrix of inputs (samples x features)
		Y         - The column vector of outputs (samples x ouptuts)
"""

import numpy as np

def gen_data(samples, features, impFeat, min_sigma=0.1, max_sigma=3, sigma_const=0.1):

	# The output matrix (samples, features)
  	X = np.empty((samples, features), float)	

	# Generation of dependant variable with uniform distribution in [-1,1]	
	Y = np.random.uniform(-1,1,samples)

	# Generation of independant variables adding white noise to
	# uniform ditribution in [0,1].  Related features are equal to
	# dependant variable with incremental white noise.
	sigma = min_sigma
	delta_sigma = (max_sigma - min_sigma)/impFeat
	
	for i in range(0, impFeat):
		X[:,i] = Y + np.random.randn(samples) * np.sqrt(sigma)
		sigma += delta_sigma	
	
	for i in range(impFeat, features):
		X[:,i] = np.random.uniform(-1,1,samples) + np.random.randn(samples) * np.sqrt(sigma_const)

	# Normalize the input to null mean and unitary standard deviation.
	meanX = np.mean(X, axis=0) 
	stdX = np.std(X, axis=0)
	#if stdX != 0:         # if it is = 0 there is a mistake somewhere
	X = (X - meanX)/stdX 		

	return Y, X
	
	

######################################################################
if __name__ == "__main__":

	# funcion testing: generate the data and test the features
	# correlation with the dependant variable
	y,x = gen_data(100,500, 20)

	corrvalues = np.zeros(x.shape[1])
	for i in range(x.shape[1]):
		corrvalues[i] = np.corrcoef(y, x[:,i])[0,1]
		pass
	print corrvalues
