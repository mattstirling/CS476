'''
Created on Dec 11, 2016

@author: Trader
'''
import numpy as np

#option Parameters
sigma = .5
r = .06
T = 1
strike_price = 100
close_price = 100

#model Parameters
timestep = .01

print np.ceil(T / timestep)