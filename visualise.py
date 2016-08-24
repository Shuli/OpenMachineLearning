# -*- coding: utf-8 -*-
"""
=============================================================================================
1.visalise
    The plot of the kernel matrix
=============================================================================================
Operating conditions necessary {UTF-8/CrLf/Python2.7/numpy/matlot/Scipy}
@author: Hisashi Ikari
"""
# Standard Library
from numpy import *
from scipy import *
from matplotlib.pyplot import *

# Custom Library
import kernel_matrix as km # Create a kernel matrix using a Gaussian kernel function
import dot_product as dp   # Calculate the inner product like Matlab/Octave in Python
import random_dist as rn   # Create the training data
import normalize as nl     # Create the kernel matrix are averaged

# ===========================================================================================
# The plot of the kernel matrix
#   The plot of the kernel matrix
# ===========================================================================================
# *** Arguments ***
#   K:Kernel Matrix
#   k:The number of components necessary
# ===========================================================================================
def visualise(K, k):
    
    N = len(K)
    D = diag([sum(K[:,i]) for i in range(N)])
    L = D - K
    
    #print "L\n", L
    
    # The kernel matrix eigenvalue decomposition, you get the eigenvalues.
    lam, V = linalg.eigh(L)
    #print "lam\n", lam
    
    # I has the dimension of the eigenvectors valid
    # *** Not available in Python ***
    I = indices(abs(lam), lambda x: x >  0.00001)

    # Returns the eigenvalues ​​obtained
    tau = V[:,1:int(k)+1]
    
    return tau

# ===========================================================================================
# Returns the same functional elements of the Find function Matlab,
# to match the comparison of the specified value in the array specified
# ===========================================================================================
def indices(a, func):
    return [i for (i, val) in enumerate(a) if func(val)]
    
# ===========================================================================================
# Reads the data file
# Data file is a newline character to separate the code that depends on the OS space and,
# given x, y, label {0,1}
# ===========================================================================================
# -------------------------------------------------------------------------------------------
# Initial processing
# -------------------------------------------------------------------------------------------
# Create the data based on two-dimensional normal distribution
# This is simple test

#A = loadtxt("training.dat")
#K = km.create_kernel_matrix(A, 1.0)
#K = nl.normalize_matrix(K)

#R = visualise(K, 3.0)

#print "R\n", R

# Draw the graph
#scatter(R[:,0], R[:,1], c='b', marker='o')
#show()
#close()

    
