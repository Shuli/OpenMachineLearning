# -*- coding: utf-8 -*-
"""
=============================================================================================
1.(Function Name)
    Description
=============================================================================================
Operating conditions necessary {UTF-8/CrLf/Python2.7/numpy/matlot/Scipy}
@author: Hisashi Ikari
"""

# ===========================================================================================
# Function Name
#   Descrption
# ===========================================================================================
# *** Arguments ***
#   Name:Description
# ===========================================================================================
import numpy as np
import quadprog as qp

K = [[10.0,5.0],[3.0,4.0]]
L = [[1.0, -1.0]]

N   = len(K)

f   = []
Aeq = np.matrix(L).T
beq = [[1, 0]]
A   = []
b   = []
LB  = np.zeros((N,1))
UB  = np.ones((N,1))/(0.3 * N)

alpha = qp.quadprog(K,f,Aeq,beq,LB,UB)

print alpha
