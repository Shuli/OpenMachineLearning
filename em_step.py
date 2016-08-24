# -*- coding: utf-8 -*-
"""
=============================================================================================
1.(Function Name)
    Description
=============================================================================================
Operating conditions necessary {UTF-8/CrLf/Python2.7/numpy/matlot/Scipy}
@author: Hisashi Ikari
"""
import math
import random 

from numpy import *
from pylab import *

# ===========================================================================================
# Function Name
#   Descrption
# ===========================================================================================
# *** Arguments ***
#   Name:Description
# ===========================================================================================
def mixture_gaussian(i):
    pi_0 = 0.3
    if random.random() < pi_0: 
        return random.gauss(-5, 1)
    else:
        return random.gauss( 5, 4)

N = 1000
x = [ mixture_gaussian(i) for i in range(N)]
#n, bins, patches = hist(x, 100, normed=1, facecolor='green', alpha=0.75)
#show()


def dnorm(x, mu, sigma2):
    return 1/math.sqrt(2*math.pi*sigma2)*math.exp(-1/(2*sigma2)*( (x-mu)**2 ))

def log_likelihood(x, mu, sigma, pi):
    return sum([math.log(pi[0] * dnorm(x[i], mu[0], sigma[0]) +
                         pi[1] * dnorm(x[i], mu[1], sigma[1]))
                for i in range(len(x))])

mu = [ -1.0, -1.0 ]
sigma = [ 1.0, 2.0 ]
pi = [ 0.5, 0.5 ]
gamma_0 = []
gamma_1 = []
n_k = [0,0]

new_log_likelihood = log_likelihood(x, mu, sigma, pi)
for step in range(1000):
    old_log_likelihood = new_log_likelihood
    
    # E-step
    gamma_0 = [ pi[0] * dnorm(x[j], mu[0], sigma[0]) /
            sum( [ pi[i] * dnorm(x[j], mu[i], sigma[i]) for i in range(2)])
            for j in range(len(x))]
    gamma_1 = map( (lambda x: 1 -x), gamma_0 )
    #print gamma_0

    # M-step
    n_k[0] = sum(gamma_0)
    n_k[1] = sum(gamma_1)
    lenx = len(x)
    mu[0] = sum( [ gamma_0[i] * x[i] / n_k[0] for i in range(lenx)])
    mu[1] = sum( [ gamma_1[i] * x[i] / n_k[1] for i in range(lenx)])
    sigma[0] = sum( [ (gamma_0[i] * (x[i] - mu[0])**2) /n_k[0] for i in range(lenx)])
    sigma[1] = sum( [ (gamma_1[i] * (x[i] - mu[1])**2) /n_k[1] for i in range(lenx)])

    pi[0] = n_k[0]/N
    pi[1] = 1 - pi[0]
    new_log_likelihood = log_likelihood(x, mu, sigma, pi)
    if(abs(new_log_likelihood - old_log_likelihood) < 0.01):
        break

print mu
print sigma
print pi
