# -*- coding: utf-8 -*-
"""
=============================================================================================
1.except_for_isolated_word
    Words do not appear only in one sentence, as you have not co-occurrence,
    frequency away from the matrix.
---------------------------------------------------------------------------------------------
2.find_dimensions_valid_singular
    Total of the D_i were obtained,
    until it reaches the specified value of the scores of the singular point,
    repeat the addition, to find the valid dimension.
=============================================================================================
Operating conditions necessary {UTF-8/CrLf/Python2.7/numpy/matlot/Scipy}
@author: Hisashi Ikari
"""
from numpy import *

# ===========================================================================================
# elimination_sparse
#    Words do not appear only in one sentence, as you have not co-occurrence,
#    frequency away from the matrix.
# ===========================================================================================
# *** Arguments ***
#   F:Frequency matrix
# ===========================================================================================
def except_for_isolated_word(F):
    NR = len(F  )
    NC = len(F.T)

    #If the word does not appear in the text of two or more disabled and that word
    for i in range(NR):
        if sum(F[i,:]) < 2:
            F[i,:] = zeros((NC))
    
    #savetxt("lsi_temp_except_for_isolated_word.txt", F, fmt="%f")    
    
    # *** Note ***
    # Originally, I would like to erase the line of the word,
    # because it does not know how to remove it, and assign all zeros.
    return F

# ===========================================================================================
# find_dimensions_valid_singular
#    Total of the column i of D were obtained,
#    until it reaches the specified value of the scores of the singular point,
#    repeat the addition, to find the valid dimension.
# ===========================================================================================
# *** Arguments ***
#   S:D'D......(for word to document)
#   V:%SIGMA...(Diagonal matrix for making the original matrix by the product of S and V)
#   S:DD'......(for document to word)
# ===========================================================================================
def find_dimensions_valid_singular(U,S,V):

    #print "D\n", D
    T = V
    N = len(T)
    
    r = -1
    t = sum(T)
    for i in range(N):
        if sum(T[:,0:i]) / t > 0.5:
            r = i
            break;
            
    # The smallest dimension is two and learn(by the) to principal component analysis
    r = 2 if r < 2 else r

    return r    
    
# ===========================================================================================
# get_cosine_distance
#   Calculates the cosine distance of the elements of the specified column.
#   Cosine distance will be the...{t / sqrt(sum(r)) * sqrt (sum(r))}. r is D[:,i].
# ===========================================================================================
# *** Arguments ***
#   T:The target element T[i,j]
# ===========================================================================================
def get_cosine_distance(T,d=False):
    NR = len(T  ) # for row numbers
    NC = len(T.T) # for column numbers
    NN = NR if NR > NC else NC

    # (*1)Here, (y) is to be lower than (x) is not a comparison of word-dimensional matrix is not performed first.
    #NN = NC if NC > NR else NR
    
    # The answer is {t / sqrt(sum(r)) * sqrt (sum(r))}
    r = zeros((NN, NN)) # (*1)
    for i in range(NR):
        for j in range(NR):
            # ...dot product...
            a = dot(T[i,:], T[j,:].T)
            b = dot(T[i,:], T[i,:].T)
            c = dot(T[j,:], T[j,:].T)

            #a = T[i,:] * T[j,:].T
            #b = T[i,:] * T[i,:].T
            #c = T[j,:] * T[j,:].T

            d = sqrt(b * c)

            if d != 0.0:
                r[i,j] = a / d

    return r

# ===========================================================================================
# get_cosine_distance
#   Calculates the cosine distance of the elements of the specified column.
#   Cosine distance will be the...{t / sqrt(sum(r)) * sqrt (sum(r))}. r is D[:,i].
# ===========================================================================================
# *** Arguments ***
#   T:The target element T[i,j]
#   t:target vector
# ===========================================================================================
def get_cosine_distance_on_target(t,T,d=True):
    NR = len(T  ) # for row numbers
    #NC = len(T.T) # for column numbers

    # (*1)Here, (y) is to be lower than (x) is not a comparison of word-dimensional matrix is not performed first.
    #NN = NC if NC > NR else NR
    
    # The answer is {t / sqrt(sum(r)) * sqrt (sum(r))}
    r = zeros((NR)) # (*1)
    for i in range(NR):
        # ...dot product...
        a = dot(t,      T[i,:].T)
        b = dot(t,      t.T)
        c = dot(T[i,:], T[i,:].T)

        #a = t      * T[i,:].T
        #b = t      * t.T
        #c = T[i,:] * T[i,:].T

        d = sqrt(b * c)
        if d != 0.0:
            r[i] = a / d

    return r

