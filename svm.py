# -*- coding: utf-8 -*-
"""
=============================================================================================
1.single_norm_soft_margin_svm
    Provides a support vector machine of "1 norm soft margin"
---------------------------------------------------------------------------------------------
    The reliability of the upper bound uses the δ(D).
    Margin is used to control C. This should be greater than or equal to 1/N normal.
    "C indicates the error is permitted. However, the optimization problem to minimize this"
    N indicates the number of specimens.
    The ease of using σ will turn. It is available in the Gaussian kernel function.    
---------------------------------------------------------------------------------------------
    *** Reference(many thanks) ***
    http://www.kernel-methods.net/
=============================================================================================
Operating conditions necessary Python(x,y){UTF-8/CrLf/Python2.7/numpy/matlotlib/scipy}
@author: Hisashi Ikari
"""
# Standard library
import sys
from numpy import *
from scipy import *
from numpy.linalg import *
from matplotlib.pyplot import *
from cvxopt import matrix as cvxmat
from cvxopt import solvers as cvxopt

# Custom library
import kernel_matrix as km # Create a kernel matrix using a Gaussian kernel function
import dot_product as dp   # Calculate the inner product like Matlab/Octave in Python
import random_dist as rn   # Create the training data

# ===========================================================================================
# Global Variable
# ===========================================================================================
# Specifies the number of training data used in learning
N = 100

# 1-δ, is constant reliability in determining the upper bound, if this is 0.01%
# the reliability of the upper bound is 99.9% This means that for example
D = 0.01 

# Slack variables, by this error term, to suppress the extreme bending of the nonlinear threshold
# Generalization performance is up for the error if you specify the maximum number allowed. 
# However, the computation time is longer
C = 0.1 # 1 > C > (1/N)

# Standard deviation is to use Gaussian kernel function
G = 0.5  # σ => The less well bent, the more difficult to bend

# ===========================================================================================
# single_norm_soft_margin_svm
#    Provides a support vector machine of soft margin
# ===========================================================================================
# *** Arguments ***
#   S:training data
#   L:tearch signal
#   T:test data
# ===========================================================================================
# *** !!! Notes on use !!! *** 
# The number of test data and the number of training data, please be the same. 
# For example, data are not available to determine the "0.0 0.0", please have the same number
# ===========================================================================================
def single_norm_soft_margin_svm(S, L, T, plot=False):
    
    #----------------------------------------------------------------------------------------
    # Create a function of the threshold of SVM
    #----------------------------------------------------------------------------------------
    # Create a (gram matrix) kernel matrix
    K = km.create_kernel_matrix(S, G)    
    N = len(K)
    
    # Create a matrix of pairs of labels
    E = dp.vector_vector_dot_product(L, L)
    
    # Perform the integration of the scalar value is not a dot product between the matrix
    H = dp.matrix_matrix_integration(K, E)
    
    # necessary to create a convex quadratic programming to determine the α,
    # variables and objectives, constraints and solve
    P = create_param_for_soft_margin(K, H, L, C)
    
    # Under the terms of the KKT, look for support vector
    # If there is a value close to 0, then it will be to support vector
    J      = P * L
    ipos   = indices(J, lambda x: x >  0.0001)
    ineg   = indices(J, lambda x: x < -0.0001)
    
    # Calculate the offset
    lam = 0.5 * sqrt(dot(dot(H,P), P))    
    # Since the offset α(slope) has been asked already, it is only the first set.
    offset = -lam * dot((K[ipos[0],:] + K[ineg[0],:]), J)

    #print "lambda\n", lam
    #print "offset\n", offset
    #print "alpha\n", P

    # This is the classification obtained from the training set
    correct = dot(K, J) + offset
    correct = sign(correct)
    #print "correct\n", correct

    # *** matlab code is shown below ********************************
    # test = T' * (P.*L) + offset
    # Raster values ​​are used instead of the dot product.
    # However, you do not know to use the statement 
    # for the raster matrix operations in Python
    # ***************************************************************
    # T must be of the dot product of the training set and test set.
    # ***************************************************************
    #M = km.create_kernel_matrix_by_dual(S, T, G)    
    #test = P * L * M + offset
    #print "test\n", test

    # Calculate the error of the result of learning
    result = zeros((1,N))
    for i in range(N):
        if L[i] != correct[0,i]:
            result[0,i] = 1
    #print "result\n", result
    print "(C =", C, ",G =", G, ")accuracy rate:", (1.0 - sum(result) / N) * 100, "(" ,sum(result) , "/", N , ")"
    buff = "C%f-G%f.csv" % (C, G)
    savetxt(buff, [C, G, (1.0 - sum(result) / N) * 100], fmt="%f")

    #----------------------------------------------------------------------------------------
    # Draw the graph the training data. This means that it is not required
    #----------------------------------------------------------------------------------------
    # There are no differences in the two class 2 and sought the original class,
    # so you can see visually, and then plotted on a graph
    #----------------------------------------------------------------------------------------
    # In addition, the chart information is available, up to two-dimensional.
    #----------------------------------------------------------------------------------------
    if plot == True:
        MR = 3.0
        
        # Draw the training data
        for i in range(N):
            if L[i] > 0:
                if result[0,i] > 0:                
                    scatter(S[i,0], S[i,1], c='r', marker='x')
                else:
                    scatter(S[i,0], S[i,1], c='r', marker='o')
            else:
                if result[0,i] > 0:
                    scatter(S[i,0], S[i,1], c='b', marker='x')
                else:
                    scatter(S[i,0], S[i,1], c='b', marker='o')
    
        # Consider the separator, and z axis in the mesh graph
        X1, X2 = meshgrid(linspace(-MR,MR,20), linspace(-MR,MR,20))
        w, h = X1.shape
        X1.resize(X1.size)
        X2.resize(X2.size)
    
        # o calculate the kernel function, such as the threshold from the value of the z axis
        Z1 = array([get_z_axis(array([x1, x2]), P, L, S, offset) for (x1, x2) in zip(X1, X2)])
        
        X1.resize((w, h))
        X2.resize((w, h))
        Z1.resize((w, h))
        CS1 = contour(X1, X2, Z1, [0.0], colors='k', linewidths=1, origin='lower')
    
        xlim(-MR, MR)
        ylim(-MR, MR)
        
        show()
        close()
    
    return P, offset    

# ===========================================================================================
# The definition for the calculation of the z-axis of 3D,
# the same kernel function create_kernel_matrix
# http://d.hatena.ne.jp/aidiary/20100503/1272889097
# ===========================================================================================
def gaussian_kernel(x, y):
    #exp(-1/(2*sigma^2)*(coord*coord')^2)
    return exp(-norm(x - y) ** 2 / (2 * (G ** 2)))

# ===========================================================================================
# In order to make the drawing of 3D, to calculate the value of the z-axis
# http://d.hatena.ne.jp/aidiary/20100503/1272889097
# ===========================================================================================
def get_z_axis(x, a, t, X, b):
    sum = 0.0
    for n in range(N):
        sum += a[n] * t[n] * gaussian_kernel(x, X[n])
    return sum + b

# ===========================================================================================
# create_param_for_soft_margin
#   To determine the threshold, we use the convex quadratic programming
# -------------------------------------------------------------------------------------------
# *** Reference(many thanks) ***
# http://d.hatena.ne.jp/se-kichi/20100306/1267858745
# http://d.hatena.ne.jp/aidiary/20100503/1272889097
# ===========================================================================================
# *** Arguments ***
#   K:kernel matrix
#   H:L'KL(K is facing the direction of the teacher signal)...(-1 or 1)
#   L:teacher signal
#   C:slack variable
# ===========================================================================================
def create_param_for_soft_margin(K, H, L, C):
    """    
    P, q, G, h, A, b = _convert(H, f, Aeq, beq, lb, ub)
    return P, q, G, h, A, b 
    results = qp(P, q, G, h, A, b)

    P = cvxmat(H)
    q = cvxmat(f)
    if Aeq is None:
        A = None
    else:
        A = cvxmat(Aeq)
    if beq is None:
        b = None
    else:
        b = cvxmat(beq)
    n = lb.size
    G = sparse([-matrix.eye(n), matrix.eye(n)])
    h = cvxmat(vstack([-lb, ub]))
    """

    # To calculate the threshold using a convex quadratic programming
    N = len(H)
    Q = cvxmat(H)
    p = cvxmat(-ones(N))
    G = cvxmat(vstack( (diag([-1.0]*N), identity(N) )))
    h = cvxmat(hstack( (zeros(N), (ones(N) * C) )))
    A = cvxmat(array(L), (1,N))
    b = cvxmat(0.0)

    sol = cvxopt.qp(Q, p, G, h, A, b)
    alpha = array(sol['x']).reshape(N)

    return alpha

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

A = loadtxt(sys.argv[1], delimiter=',')
L = loadtxt("label.dat")
T = A

N = len(A)
print 'size:', N

a, b = single_norm_soft_margin_svm(A, L, T, True)

