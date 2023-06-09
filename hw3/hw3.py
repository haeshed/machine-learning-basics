import numpy as np


class conditional_independence():

    def __init__(self):

        # You need to fill the None value with *valid* probabilities
        self.X = {0: 0.3, 1: 0.7}  # P(X=x)
        self.Y = {0: 0.3, 1: 0.7}  # P(Y=y)
        self.C = {0: 0.5, 1: 0.5}  # P(C=c)

        self.X_Y = {
            (0, 0): 0.25,
            (0, 1): 0.25,
            (1, 0): 0.25,
            (1, 1): 0.25
        }  # P(X=x, Y=y)

        self.X_C = {
            (0, 0): 0.25,
            (0, 1): 0.25,
            (1, 0): 0.25,
            (1, 1): 0.25
        }  # P(X=x, C=y)

        self.Y_C = {
            (0, 0): 0.25,
            (0, 1): 0.25,
            (1, 0): 0.25,
            (1, 1): 0.25
        }  # P(Y=y, C=c)

        self.X_Y_C = {
            (0, 0, 0): self.X_C[(0, 0)] * self.Y_C[(0, 0)] / self.C[0],
            (0, 0, 1): self.X_C[(0, 1)] * self.Y_C[(0, 1)] / self.C[1],
            (0, 1, 0): self.X_C[(0, 0)] * self.Y_C[(1, 0)] / self.C[0],
            (0, 1, 1): self.X_C[(0, 1)] * self.Y_C[(1, 1)] / self.C[1],
            (1, 0, 0): self.X_C[(1, 0)] * self.Y_C[(0, 0)] / self.C[0],
            (1, 0, 1): self.X_C[(1, 1)] * self.Y_C[(0, 1)] / self.C[1],
            (1, 1, 0): self.X_C[(1, 0)] * self.Y_C[(1, 0)] / self.C[0],
            (1, 1, 1): self.X_C[(1, 1)] * self.Y_C[(1, 1)] / self.C[1],
        }  # P(X=x, Y=y, C=c)

    def is_X_Y_dependent(self):
        """
        return True iff X and Y are depndendent
        """
        X = self.X
        Y = self.Y
        X_Y = self.X_Y
        ###########################################################################
        # TODO: Implement the function.                                           #
        ###########################################################################
        for x_k, y_k in X_Y.keys():
            if not np.isclose(X[x_k] * Y[y_k], X_Y[(x_k, y_k)]):
                return True
        return False
        ###########################################################################
        #                             END OF YOUR CODE                            #
        ###########################################################################

    def is_X_Y_given_C_independent(self):
        """
        return True iff X_given_C and Y_given_C are indepndendent
        """
        X = self.X
        Y = self.Y
        C = self.C
        X_C = self.X_C
        Y_C = self.Y_C
        X_Y_C = self.X_Y_C
        ###########################################################################
        # TODO: Implement the function.                                           #
        ###########################################################################
        for x_k, y_k, c_k in X_Y_C.keys():
            if not np.isclose(X_Y_C[(x_k, y_k, c_k)], (X_C[(x_k, c_k)] * Y_C[(y_k, c_k)] / C[c_k])):
                return False
        return True
        ###########################################################################
        #                             END OF YOUR CODE                            #
        ###########################################################################


def poisson_log_pmf(k, rate):
    """
    k: A discrete instance
    rate: poisson rate parameter (lambda)

    return the log pmf value for instance k given the rate
    """
    log_p = None
    ###########################################################################
    # TODO: Implement the function.                                           #
    ###########################################################################
    k_fact_log = np.log(np.array([np.math.factorial(k_i) for k_i in k]))
    log_p = k * np.log(rate) - rate - k_fact_log
    ###########################################################################
    #                             END OF YOUR CODE                            #
    ###########################################################################
    return log_p


def get_poisson_log_likelihoods(samples, rates):
    """
    samples: set of univariate discrete observations
    rates: an iterable of rates to calculate log-likelihood by.

    return: 1d numpy array, where each value represent that log-likelihood value of rates[i]
    """
    likelihoods = None
    ###########################################################################
    # TODO: Implement the function.                                           #
    ###########################################################################
    likelihoods = []
    for rate in rates:
        likelihoods.append(np.sum(poisson_log_pmf(samples, rate)))
    ###########################################################################
    #                             END OF YOUR CODE                            #
    ###########################################################################
    return likelihoods


def possion_iterative_mle(samples, rates):
    """
    samples: set of univariate discrete observations
    rate: a rate to calculate log-likelihood by.

    return: the rate that maximizes the likelihood 
    """
    rate = 0.0
    likelihoods = get_poisson_log_likelihoods(samples, rates)  # might help
    ###########################################################################
    # TODO: Implement the function.                                           #
    ###########################################################################
    max_likelihood_ind = np.argmax(likelihoods)
    rate = rates[max_likelihood_ind]
    ###########################################################################
    #                             END OF YOUR CODE                            #
    ###########################################################################
    return rate


def possion_analytic_mle(samples):
    """
    samples: set of univariate discrete observations

    return: the rate that maximizes the likelihood
    """
    mean = None
    ###########################################################################
    # TODO: Implement the function.                                           #
    ###########################################################################
    mean = np.mean(samples)
    ###########################################################################
    #                             END OF YOUR CODE                            #
    ###########################################################################
    return mean


def normal_pdf(x, mean, std):
    """
    Calculate normal desnity function for a given x, mean and standrad deviation.

    Input:
    - x: A value we want to compute the distribution for.
    - mean: The mean value of the distribution.
    - std:  The standard deviation of the distribution.

    Returns the normal distribution pdf according to the given mean and std for the given x.    
    """
    p = None
    ###########################################################################
    # TODO: Implement the function.                                           #
    ###########################################################################
    p = np.square(x-mean)
    p = -p/(2*std**2)
    p = np.exp(p)
    p = p/(np.sqrt(2*np.pi)*std)
    ###########################################################################
    #                             END OF YOUR CODE                            #
    ###########################################################################
    return p


class NaiveNormalClassDistribution():
    def __init__(self, dataset, class_value):
        """
        A class which encapsulates the relevant parameters(mean, std) for a class conditinoal normal distribution.
        The mean and std are computed from a given data set.

        Input
        - dataset: The dataset as a 2d numpy array, assuming the class label is the last column
        - class_value : The class to calculate the parameters for.
        """
        ###########################################################################
        # TODO: Implement the function.                                           #
        ###########################################################################
        self.dataset = dataset
        self.class_value = class_value
        self.class_set = dataset[dataset[:, -1] == class_value][:, :-1]
        self.mean = np.mean(self.class_set, axis=0)
        self.std = np.std(self.class_set, axis=0)
        ###########################################################################
        #                             END OF YOUR CODE                            #
        ###########################################################################

    def get_prior(self):
        """
        Returns the prior porbability of the class according to the dataset distribution.
        """
        prior = None
        ###########################################################################
        # TODO: Implement the function.                                           #
        ###########################################################################
        prior = self.class_set.shape[0] / self.dataset.shape[0]
        ###########################################################################
        #                             END OF YOUR CODE                            #
        ###########################################################################
        return prior

    def get_instance_likelihood(self, x):
        """
        Returns the likelihhod porbability of the instance under the class according to the dataset distribution.
        """
        likelihood = None
        ###########################################################################
        # TODO: Implement the function.                                           #
        ###########################################################################
        likelihood = normal_pdf(x, self.mean, self.std)
        likelihood = np.prod(likelihood)
        ###########################################################################
        #                             END OF YOUR CODE                            #
        ###########################################################################
        return likelihood

    def get_instance_posterior(self, x):
        """
        Returns the posterior porbability of the instance under the class according to the dataset distribution.
        * Ignoring p(x)
        """
        posterior = None
        ###########################################################################
        # TODO: Implement the function.                                           #
        ###########################################################################
        posterior = self.get_instance_likelihood(x) * self.get_prior()
        ###########################################################################
        #                             END OF YOUR CODE                            #
        ###########################################################################
        return posterior


class MAPClassifier():
    def __init__(self, ccd0, ccd1):
        """
        A Maximum a posteriori classifier. 
        This class will hold 2 class distributions. 
        One for class 0 and one for class 1, and will predict an instance
        using the class that outputs the highest posterior probability 
        for the given instance.

        Input
            - ccd0 : An object contating the relevant parameters and methods 
                     for the distribution of class 0.
            - ccd1 : An object contating the relevant parameters and methods 
                     for the distribution of class 1.
        """
        ###########################################################################
        # TODO: Implement the function.                                           #
        ###########################################################################
        self.ccd0 = ccd0
        self.ccd1 = ccd1
        ###########################################################################
        #                             END OF YOUR CODE                            #
        ###########################################################################

    def predict(self, x):
        """
        Predicts the instance class using the 2 distribution objects given in the object constructor.

        Input
            - An instance to predict.
        Output
            - 0 if the posterior probability of class 0 is higher and 1 otherwise.
        """
        pred = 1
        ###########################################################################
        # TODO: Implement the function.                                           #
        ###########################################################################
        if (self.ccd0.get_instance_posterior(x) > self.ccd1.get_instance_posterior(x)):
            pred = 0
        ###########################################################################
        #                             END OF YOUR CODE                            #
        ###########################################################################
        return pred


def compute_accuracy(test_set, map_classifier):
    """
    Compute the accuracy of a given a test_set using a MAP classifier object.

    Input
        - test_set: The test_set for which to compute the accuracy (Numpy array). where the class label is the last column
        - map_classifier : A MAPClassifier object capable of prediciting the class for each instance in the testset.

    Ouput
        - Accuracy = #Correctly Classified / test_set size
    """
    acc = 0
    ###########################################################################
    # TODO: Implement the function.                                           #
    ###########################################################################
    for i in test_set:
        if map_classifier.predict(i[:-1]) == i[-1]:
            acc = acc+1
    acc = acc/test_set.shape[0]
    ###########################################################################
    #                             END OF YOUR CODE                            #
    ###########################################################################
    return acc


def multi_normal_pdf(x, mean, cov):
    """
    Calculate multi variable normal desnity function for a given x, mean and covarince matrix.

    Input:
    - x: A value we want to compute the distribution for.
    - mean: The mean vector of the distribution.
    - cov:  The covariance matrix of the distribution.

    Returns the normal distribution pdf according to the given mean and var for the given x.    
    """
    pdf = None
    ###########################################################################
    # TODO: Implement the function.                                           #
    ###########################################################################
    dim = len(cov)
    cov_inv = np.linalg.inv(cov)
    exponent = np.exp(np.dot(np.dot((x - mean).T, cov_inv), x - mean))
    constants = (2 * np.pi) ** dim * np.linalg.det(cov)
    pdf = 1 / np.sqrt(constants * exponent)
    ###########################################################################
    #                             END OF YOUR CODE                            #
    ###########################################################################
    return pdf


class MultiNormalClassDistribution():

    def __init__(self, dataset, class_value):
        """
        A class which encapsulate the relevant parameters(mean, cov matrix) for a class conditinoal multi normal distribution.
        The mean and cov matrix (You can use np.cov for this!) will be computed from a given data set.

        Input
        - dataset: The dataset as a numpy array
        - class_value : The class to calculate the parameters for.
        """
        ###########################################################################
        # TODO: Implement the function.                                           #
        ###########################################################################
        self.dataset = dataset
        self.class_value = class_value
        self.class_set = dataset[dataset[:, -1] == class_value][:, :-1]
        self.mean = np.mean(self.class_set, axis=0)
        self.cov_matrix = np.cov(self.class_set.T)
        ###########################################################################
        #                             END OF YOUR CODE                            #
        ###########################################################################

    def get_prior(self):
        """
        Returns the prior porbability of the class according to the dataset distribution.
        """
        prior = None
        ###########################################################################
        # TODO: Implement the function.                                           #
        ###########################################################################
        prior = self.class_set.shape[0] / self.dataset.shape[0]
        ###########################################################################
        #                             END OF YOUR CODE                            #
        ###########################################################################
        return prior

    def get_instance_likelihood(self, x):
        """
        Returns the likelihood of the instance under the class according to the dataset distribution.
        """
        likelihood = None
        ###########################################################################
        # TODO: Implement the function.                                           #
        ###########################################################################
        likelihood = multi_normal_pdf(x, self.mean, self.cov_matrix)
        ###########################################################################
        #                             END OF YOUR CODE                            #
        ###########################################################################
        return likelihood

    def get_instance_posterior(self, x):
        """
        Returns the posterior porbability of the instance under the class according to the dataset distribution.
        * Ignoring p(x)
        """
        posterior = None
        ###########################################################################
        # TODO: Implement the function.                                           #
        ###########################################################################
        posterior = self.get_prior() * self.get_instance_likelihood(x)
        ###########################################################################
        #                             END OF YOUR CODE                            #
        ###########################################################################
        return posterior


class MaxPrior():
    def __init__(self, ccd0, ccd1):
        """
        A Maximum prior classifier. 
        This class will hold 2 class distributions, one for class 0 and one for class 1, and will predicit an instance
        by the class that outputs the highest prior probability for the given instance.

        Input
            - ccd0 : An object contating the relevant parameters and methods for the distribution of class 0.
            - ccd1 : An object contating the relevant parameters and methods for the distribution of class 1.
        """
        ###########################################################################
        # TODO: Implement the function.                                           #
        ###########################################################################
        self.ccd0 = ccd0
        self.ccd1 = ccd1
        ###########################################################################
        #                             END OF YOUR CODE                            #
        ###########################################################################

    def predict(self, x):
        """
        Predicts the instance class using the 2 distribution objects given in the object constructor.

        Input
            - An instance to predict.
        Output
            - 0 if the posterior probability of class 0 is higher and 1 otherwise.
        """
        pred = 1
        ###########################################################################
        # TODO: Implement the function.                                           #
        ###########################################################################
        if (self.ccd0.get_prior() > self.ccd1.get_prior()):
            pred = 0
        ###########################################################################
        #                             END OF YOUR CODE                            #
        ###########################################################################
        return pred


class MaxLikelihood():
    def __init__(self, ccd0, ccd1):
        """
        A Maximum Likelihood classifier. 
        This class will hold 2 class distributions, one for class 0 and one for class 1, and will predicit an instance
        by the class that outputs the highest likelihood probability for the given instance.

        Input
            - ccd0 : An object contating the relevant parameters and methods for the distribution of class 0.
            - ccd1 : An object contating the relevant parameters and methods for the distribution of class 1.
        """
        ###########################################################################
        # TODO: Implement the function.                                           #
        ###########################################################################
        self.ccd0 = ccd0
        self.ccd1 = ccd1
        ###########################################################################
        #                             END OF YOUR CODE                            #
        ###########################################################################

    def predict(self, x):
        """
        Predicts the instance class using the 2 distribution objects given in the object constructor.

        Input
            - An instance to predict.
        Output
            - 0 if the posterior probability of class 0 is higher and 1 otherwise.
        """
        pred = 1
        ###########################################################################
        # TODO: Implement the function.                                           #
        ###########################################################################
        if (self.ccd0.get_instance_likelihood(x) > self.ccd1.get_instance_likelihood(x)):
            pred = 0
        ###########################################################################
        #                             END OF YOUR CODE                            #
        ###########################################################################
        return pred


# if a certain value only occurs in the test set, the probability for that value will be EPSILLON.
EPSILLON = 1e-6


class DiscreteNBClassDistribution():
    def __init__(self, dataset, class_value):
        """
        A class which computes and encapsulate the relevant probabilites for a discrete naive bayes 
        distribution for a specific class. The probabilites are computed with laplace smoothing.

        Input
        - dataset: The dataset as a numpy array.
        - class_value: Compute the relevant parameters only for instances from the given class.
        """
        ###########################################################################
        # TODO: Implement the function.                                           #
        ###########################################################################
        self.dataset = dataset
        self.class_value = class_value
        self.class_set = dataset[dataset[:, -1] == class_value][:, :-1]
        ###########################################################################
        #                             END OF YOUR CODE                            #
        ###########################################################################

    def get_prior(self):
        """
        Returns the prior porbability of the class 
        according to the dataset distribution.
        """
        prior = None
        ###########################################################################
        # TODO: Implement the function.                                           #
        ###########################################################################
        prior = self.class_set.shape[0] / self.dataset.shape[0]
        ###########################################################################
        #                             END OF YOUR CODE                            #
        ###########################################################################
        return prior

    def get_instance_likelihood(self, x):
        """
        Returns the likelihood of the instance under 
        the class according to the dataset distribution.
        """
        likelihood = None
        ###########################################################################
        # TODO: Implement the function.                                           #
        ###########################################################################
        class_set = self.class_set
        feature_prob = []
        for feature_idx in range(self.dataset.shape[1] - 1):
            feature_uniq_vals = np.unique(self.dataset[:, feature_idx])
            if x[feature_idx] in feature_uniq_vals:
                n_ij = len(class_set[class_set[:, feature_idx] == x[feature_idx]])
                feature_prob.append((n_ij + 1) / (len(class_set) + len(feature_uniq_vals)))
            else:
                feature_prob.append(EPSILLON)
        likelihood = np.prod(np.array(feature_prob))
        ###########################################################################
        #                             END OF YOUR CODE                            #
        ###########################################################################
        return likelihood

    def get_instance_posterior(self, x):
        """
        Returns the posterior porbability of the instance 
        under the class according to the dataset distribution.
        * Ignoring p(x)
        """
        posterior = None
        ###########################################################################
        # TODO: Implement the function.                                           #
        ###########################################################################
        posterior = self.get_instance_likelihood(x) * self.get_prior()
        ###########################################################################
        #                             END OF YOUR CODE                            #
        ###########################################################################
        return posterior


class MAPClassifier_DNB():
    def __init__(self, ccd0, ccd1):
        """
        A Maximum a posteriori classifier. 
        This class will hold 2 class distributions, one for class 0 and one for class 1, and will predict an instance
        by the class that outputs the highest posterior probability for the given instance.

        Input
            - ccd0 : An object contating the relevant parameters and methods for the distribution of class 0.
            - ccd1 : An object contating the relevant parameters and methods for the distribution of class 1.
        """
        ###########################################################################
        # TODO: Implement the function.                                           #
        ###########################################################################
        self.ccd0 = ccd0
        self.ccd1 = ccd1
        ###########################################################################
        #                             END OF YOUR CODE                            #
        ###########################################################################

    def predict(self, x):
        """
        Predicts the instance class using the 2 distribution objects given in the object constructor.

        Input
            - An instance to predict.
        Output
            - 0 if the posterior probability of class 0 is higher and 1 otherwise.
        """
        pred = 1
        ###########################################################################
        # TODO: Implement the function.                                           #
        ###########################################################################
        if (self.ccd0.get_instance_posterior(x) > self.ccd1.get_instance_posterior(x)):
            pred = 0
        ###########################################################################
        #                             END OF YOUR CODE                            #
        ###########################################################################
        return pred

    def compute_accuracy(self, test_set):
        """
        Compute the accuracy of a given a testset using a MAP classifier object.

        Input
            - test_set: The test_set for which to compute the accuracy (Numpy array).
        Ouput
            - Accuracy = #Correctly Classified / #test_set size
        """
        acc = 0
        ###########################################################################
        # TODO: Implement the function.                                           #
        ###########################################################################
        for i in test_set:
            if self.predict(i[:-1]) == i[-1]:
                acc = acc+1
        acc = acc/test_set.shape[0]
        ###########################################################################
        #                             END OF YOUR CODE                            #
        ###########################################################################
        return acc
