# -*- coding: utf-8 -*-
"""
=============================================================================================
1.create_dot_product
    Create an dot product matrix from "the training set and test set".
2.custom_dot_product
    Calculates the dot product of vector dot product like a matrix
=============================================================================================
Operating conditions necessary{UTF-8/CrLf/Python2.7/numpy/matlot/Scipy}
@author: Hisashi Ikari
"""
import numpy as np

# ===========================================================================================
# Create an dot product matrix from "the training set and test set".
# The usual dot product matrix is created from the training set 
# and test set. However, "the last column is the dot product 
# of the test set and test set".
# -------------------------------------------------------------------------------------------
# ***Arguments***
#   A:Traning data
#   B:Test data
#   return:B * A' ..."row appended(B * B')"
# ===========================================================================================
def create_custom_dot_product(A, B):
    N = len(A)
    
    # To calculate the dot product using the RBF kernel function
    K = np.dot(B, A.T)
    # Dot product of the test set will use the diagonal
    T = np.diag(np.dot(B, B.T))
    # The last line is a dot product of the test set and test set.
    # For this reason, and assign it as the dot product of its diagonal line.
    K.resize(N + 1, N)
    K[N] = T
    
    return K

# ===========================================================================================
# Calculates the dot product of vector dot product like a matrix
# *** Create a matrix from vector integration between ***
# -------------------------------------------------------------------------------------------
# *** Definition ***
#   A:vector(one-dimensional)
#   B:vector(one-dimensional)
#   return:"Matrix"
# ===========================================================================================
def vector_vector_dot_product(A, B):
    N1 = len(A)    
    N2 = len(B)    
    K = np.zeros((N1, N2))
    for i in range(N1):
        for j in range(N2):
            K[i, j] = A[i] * B[j]
            
    return K

# ===========================================================================================
# Calculates the dot product of vector dot product like a matrix
# *** Create a matrix from vector integration between ***
# -------------------------------------------------------------------------------------------
# *** Definition ***
#   A:matrix(same-vector-dimensional)
#   B:vector(one-dimensional)
#   return:vector
# ===========================================================================================
def vector_matrix_dot_product(M, V):
    N = len(M)    
    R = np.zeros((N))
    for i in range(N):     # column
        st = 0
        for j in range(N): # row
            st += M[j, i] * V[j]
        R[i] = st
    return R
    
# ===========================================================================================
# Calculate the number of inner product of a matrix not aligned
# -------------------------------------------------------------------------------------------
# *** Definition ***
#   A:matrix
#   B:matrix'
#   return:matrix
# ===========================================================================================
def matrix_matrix_dot_product(A, B):
    NL = len(A[:,0])    
    NC = len(A[0,:])    
    N = NL if (NL > NC) else NC
    
    K = np.zeros((N, N))
    for i in range(NL):
        for j in range(NC):
            K[i, j] += A[i, j] + B[j, i]

    return K
    
# ===========================================================================================
# Calculate the number of inner product of a matrix not aligned
# -------------------------------------------------------------------------------------------
# *** Definition ***
#   A:matrix
#   B:matrix'
#   return:matrix
# ===========================================================================================
def matrix_matrix_integration(A, B):
    N = len(A)    
    K = np.zeros((N, N))
    for i in range(N):
        for j in range(N):
            K[i, j] = A[i, j] * B[i, j]
    return K

# ===========================================================================================
# Calculate the number of inner product of a matrix not aligned
# -------------------------------------------------------------------------------------------
# *** Definition ***
#   A:matrix
#   B:matrix'
#   return:matrix
# ===========================================================================================
def matrix_matrix_mn_integration(A, B):
    NA = len(A[0,:])    
    NB = len(B[0,:])    
    NR = len(A)

    K = np.zeros((NR, NA))
    for i in range(NR):     # row
        for j in range(NA): # column
            K[i, j] = A[i, j] * B[j, j]
    return K


    
