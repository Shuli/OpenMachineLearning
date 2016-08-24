# -*- coding: utf-8 -*-
"""
=============================================================================================
1.anova
    ANOVA is an implementation of the kernel. ANOVA kernel shows the calculations based on
    the "dynamic programming" recursion, we further remove the unnecessary computations.    
=============================================================================================
Operating conditions necessary {UTF-8/CrLf/Python2.7/numpy/matlot/Scipy}
@author: Hisashi Ikari
"""
from numpy import *

# ===========================================================================================
# anova
#   ANOVA is an implementation of the kernel. ANOVA kernel shows the calculations based on
#   the "dynamic programming" recursion, we further remove the unnecessary computations.    
# ===========================================================================================
# *** Arguments ***
#   s:x_n(any number) Ex.[5 4]
#   t:z_n(any number) Ex [3 2]
#   p:dimension
# ===========================================================================================
# *** Description ***
# -------------------------------------------------------------------------------------------
#   definition of recursive
#       k_s^{m} (x,z) = K_s(x_{1:m},z_{1:m})
# -------------------------------------------------------------------------------------------
#   definition of anova
#       k_0^{m}(x,z) = 1 (when m >= 0)
#       k_s^{m}(x,z) = 0 (when m <  0)
#       k_s^{m}(x,z) = (x_m z_m) k_s-1^{m-1}(x,z) + k_s^{m-1}(x,z)
# ===========================================================================================
def anova(s, t, p):
    n = len(s)
    m = len(t)

    # Initialized to -1 would the answer to all of the area
    # This is because it contains a 0 in the answer, we have an initial value of -1
    K = kron(ones((p,n,m)), -1)
    #print "K\n", K

    for h in range(p):
        for i in range(n):
            for j in range(i,m):
                K[h,i,j] = anova_kernel(s[0:i+1], t[0:j+1], K, h)

    #print "answer\n", K[p-1,n-1,m-1]
    return K[p-1,:,:], K[p-1,n-1,m-1]

# ===========================================================================================
# anova_kernel
#   Run the ANOVA kernel recursion. To perform recursive processing, 
#   the matrix that is passed every one hierarchy, will be the next one down.
# ===========================================================================================
# *** Arguments ***
#   sd:x_n(any number) Ex.[5 4] ...But If the one-dimensional reduced to [5]
#   td:z_n(any number) Ex.[3 2] ...But If the one-dimensional reduced to [3]
# ===========================================================================================
def anova_kernel(sd, td, K, p):
    n = len(sd)
    m = len(td)       

    s = sd[0:n-1]
    t = td[0:m-1]

    nd = len(s) 
    md = len(t)

    # ---------------------------------------------------------------------------------------
    # We will seek answers to the following table in order to calculate
    # ---------------------------------------------------------------------------------------
    # DP    |   m=1       2                ...         n
    #--------------------------------------------------------------------
    # S=0   |   1         1                ...         1
    #  1    |   x_1*z_1   x_1*z_1+x_2*z_2  ...         Σ csup{n} x_i*z_i
    #  2    |   0         k_2^{2}(x,z)     ...         k_2^{n}(x,z)
    # ...   |   ...       ...              ...         ...
    #  d    |   0         0                ...         k_d^{n}(x,z)
    # ---------------------------------------------------------------------------------------
    r1 = 0                       if nd == 0 or md == 0     else \
         anova_kernel(s,t,K,p)   if K[p-1,nd-1,md-1] == -1 else \
         K[p-0,nd-1,md-1]
         
    k = sd[n-1] * td[m-1] 
    
    r2 = 1                       if p  == 0                else \
         0                       if nd == 0 or md == 0     else \
         anova_kernel(s,t,K,p-1) if K[p-1,nd-1,md-1] == -1 else \
         K[p-1,nd-1,md-1]
         
    r1 = r1 + (k * r2)        
    #print "answer", r1
    
    return r1
    
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

#R = anova([5,4], [3,2], 2)
#R = anova([5,4,3], [3,2,1], 2)

R, r = anova([5,4,3,2], [3,2,1,0], 2)
print "R\n", R
print "r\n", r

