# -*- coding: utf-8 -*-
"""
=============================================================================================
1.normalize_matrix
    Returns a random number from a two-dimensional normal distribution
=============================================================================================
Operating conditions necessary {UTF-8/CrLf/Python2.7/numpy/matlot/Scipy}
@author: Hisashi Ikari
"""
import numpy as np

# ===========================================================================================
# Returns a random number from a two-dimensional normal distribution 
# is specified mean and covariance
# -------------------------------------------------------------------------------------------
# *** Arguments ***
#   num:The number of random numbers
#   mean:This is the average of the normal distribution
#   cov:This is the covariance of the normal distribution
# ===========================================================================================
def create_multivariate_normal(num, mean = [0,0], cov = [[2,1],[1,2]]):
    nomarize = np.random.multivariate_normal(mean,cov,num)
    return nomarize   
