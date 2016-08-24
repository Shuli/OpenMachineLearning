# -*- coding: utf-8 -*-
"""
=============================================================================================
1.duallsi
    To decompose the kernel matrix given singular point,
    find the same meaning than its frequency.
2.create_kernel_matrix
    
=============================================================================================
Operating conditions necessary {UTF-8/CrLf/Python2.7/numpy/matlot/Scipy}
@author: Hisashi Ikari
"""
import sys
import codecs

from numpy import *
from scipy import linalg

import normalize as nm

# ===========================================================================================
# duallsi
#   Performed based on the kernel matrix decomposition singular point,
#   find the dot product of each other's word. Returns the matrix of the results obtained from it.  
# -------------------------------------------------------------------------------------------
# *** Reference(many thanks) ***
# http://d.hatena.ne.jp/billest/20090819/1250635423
# ===========================================================================================
# *** Supplemental ***
#   - Matrix defined frequency, co-occurrence matrix - 
#       (D'D)_{i,j} = %SIGMA tf(i,d) tf(j,d) ...d=document, tf=frequency
#   - SVD - 
#       D' = UZV'
#   - Latent semantic analysis by the proximity matrix -
#       P = U_k U_k'
# -------------------------------------------------------------------------------------------
# *** Arguments ***
#   F:frequency matrix
#   k:Number of dimensions you want to compress(This indicates the amount of the smoothness of the meaning)
# ===========================================================================================
def duallsi(F, k):
    # ---------------------------------------------------------------------------------------
    # Frequency matrix U can be calculated the dot product of the inner product 
    # without asking for sparse matrix, obtained by the decomposition singularity.
    # ---------------------------------------------------------------------------------------
    #E = dot(F, F.T) 
    #E = nm.normalize_matrix(E)
    E = F
    print "E\n", E
    
    # ---------------------------------------------------------------------------------------
    # The singular point decomposition
    # ---------------------------------------------------------------------------------------
    U,S,V = linalg.svd(E)
    R = shape (F)[0]
    U = matrix(U)
    S = matrix(linalg.diagsvd(S,R,R))
    V = matrix(V[:R,:])
    
    # ---------------------------------------------------------------------------------------
    # Create a proximity matrix in search of inner product of U.
    # Save the file temporarily to avoid the need of this computation.
    # ---------------------------------------------------------------------------------------
    #print "U,len(U)\n", U, len(U)
    #print "S\n", S
    #print "V\n", V
    print "U*S*V\n", U*S*V

    savetxt("duallsi_result_u.txt", U, fmt="%f")

    #U = U[:,:k]    
    R = U #* U.T
    #R = U
    #print "U*U.T\n", U * U.T
    
    return R

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

print "=" * 70
print "Start of treatment"
print "=" * 70

# Gets a matrix of frequency of occurrence of a word document
T = loadtxt("result_mecab_frequency.txt")
print "T\n", T

R = duallsi(T, 10)
savetxt("duallsi_result_matrix.txt", R, fmt="%f")
#R = loadtxt("duallsi_result_matrix.txt")

# -------------------------------------------------------------------------------------------
# The user selects the word
# -------------------------------------------------------------------------------------------
# Gets the unique words that appear in the document
words = []
#for line in codecs.open("result_mecab_words.txt", "r", "utf-8"):
for line in open("result_mecab_words.txt", "r"):
    words.append(line)

for i in range(len(words)):
    print "%d:%s" % (i, words[i]),    

while True:
    print "=" * 70
    t = int(raw_input("index of word:"))
    print "target->%d:%s" % (t, words[t])

    s = {}
    for i in range(len(R)):
        s[i] = R[t,i] * T[t,i]
    
    i = 0
    for k,v in sorted(s.items(),key=lambda x:x[1]):
        print words[i],v
        i = i + 1
        if (i > 10):
            break

print "=" * 70
print "The end of the process"
print "=" * 70

