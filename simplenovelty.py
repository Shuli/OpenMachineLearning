# -*- coding: utf-8 -*-
"""
=============================================================================================
1.simplenovelty_kernel_matrix
    From simple novelty detection algorithm, a novel test to get the point
=============================================================================================
Operating conditions necessary {UTF-8/CrLf/Python2.7/numpy/matlot/Scipy}
@author: Hisashi Ikari
"""
import numpy as np

# ===========================================================================================
# From simple novelty detection algorithm, a novel test to get the point
# -------------------------------------------------------------------------------------------
# *** Definition of novelty detection algorithm ***
#   1.(Rtrain)^2 = k(x,x) + (1/l^2)Σ_l k(x_i, x_j)
#                - (2/l)Σ_l k(x,x_i) 
#   2."Estimated error" = sqrt(2R^2/l) (sqrt(2)+sqrt(ln(1/l)))
#   3."Squared threshold" = (max_{1<i<=l} ||R||+2 * EstimInner product matrixated error)^2
#   4.(Rtest)^2 = k(x_mboxtest, x_test) + (1/l^2)Σ_l k(x_i, x_j)
#               - (2/l)Σ_l k(x_test, x_i)
#   5.novelIndics = ((R_test)^2) >= "Meet the threshold test set of squares"
# -------------------------------------------------------------------------------------------
# *** Definition ***
#   K：Kernel matrix of training points
#   Ktest：dot product matrix of (N +1) xt of t test points of each point and the training of N
#   D：Row vector of column to store the average K
#   E：Scalar value of the average of all the components of K
# ===========================================================================================
def simplenovelty_kernel_matrix(K, Ktest):
    # ---------------------------------------------------------------------------------------
    # !!!Considerations!!!
    # ---------------------------------------------------------------------------------------
    # Test point is from a given data up to L max_ {1 <= i <= L} in. In addition,
    # K is the data from one up to L.
    # this example has "i + 1" and the L.
    # ---------------------------------------------------------------------------------------
    # Each set of initial values
    delta = 0.01
    N = len(K)
    D = np.sum(K) / N
    E = np.sum(D) / N

    traindist2 = np.diag(K) - 2 * D.T + E * np.ones((N, 1))
    maxdist = np.sqrt(np.max(traindist2))
    #print "traindist2\n", traindist2
    #print "maxdist", maxdist    

    # Center of mass to calculate the estimated error of empirical    
    esterr = np.sqrt(2 * np.max(np.diag(K)) / N) * (np.sqrt(2) + np.sqrt(np.log(1 / delta)))
    #print "esterr", esterr    
    
    # To calculate the threshold of the results
    threshold = maxdist + 2 * esterr
    threshold = threshold * threshold
    #print "threshold", threshold
    
    # To calculate the distance between the test data
    t = len(Ktest)
    
    # Holds for each column the ”total of rows” in the” training　set”
    Dtest1 = np.zeros((N)) 
    Dtest2 = np.zeros((N)) 
    for i in range(N):
        Dtest1[i] = np.sum(Ktest[0:(N-1),i]) / N
        Dtest2[i] = np.sum(Ktest[(N-1):(t-1),i])

    #print "Dtest1\n", Dtest1
    #print "Dtest2\n", Dtest2

    testdist2 = Dtest2 - 2 * Dtest1 + E * np.ones((1, N))
    #print "testdist2\n", testdist2
    print "threshold", threshold
    
    novelindices = indices(testdist2[0], lambda x: x > threshold)
    #print "novelindices", novelindices
    
    return novelindices

# ===========================================================================================
# Returns the same functional elements of the Find function Matlab,
# to match the comparison of the specified value in the array specified
# ===========================================================================================
def indices(a, func):
    return [i for (i, val) in enumerate(a) if func(val)]
