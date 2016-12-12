'''
Created on Dec 11, 2016

@author: Trader
'''
from math import sqrt
from math import exp
from math import ceil
from math import pow
import numpy as np

def bin_price_476(s_price_0,strike,r,t,timestep,sigma,is_call,is_american_exercise):
    '''
    Usage:  binprice476(S0,X,R,T,DT,SIGMA,FLAG,EXERCISE)
    This method uses a binomial lattice to price
    European/American puts and calls
     
    it is assumed that the underlying asset does not pay dividends
    
    s_price_0 - underlying price at time=0
    strike - strike of the option
    r - cts risk-free rate, in decimal form
    t - time to maturity in years
    dt - time-step used
    sigma - annual standard deviation of returns
    is_call=1 -> Call and is_call=0 -> Put
    is_american_exercise=1->American is_american_exercise=0 -> European
    
    '''
    #determine simulation variables
    num_steps = int(ceil(t/timestep))
    up_step = exp(sigma*sqrt(timestep))
    down_step = exp(-1*sigma*sqrt(timestep))
    p = (exp(r*timestep)-down_step) / (up_step-down_step) #p is the no-arb weight
    put_adj_mult = int(pow(-1,(1-is_call))) 
    
    #initialize payout vectors, vector length is num_steps + 1
    s_t_arr = np.fromiter([s_price_0*pow(up_step,num_steps-i)*pow(down_step,i) for i in xrange(num_steps+1)]
                                     ,dtype=np.float, count=num_steps+1)
    
    print s_t_arr
    
    V_arr = np.maximum(put_adj_mult*(s_t_arr-strike),np.zeros(num_steps+1))
    
    if is_american_exercise==0:
        #European case
        for i in xrange(num_steps):
            print V_arr
            V_arr = exp(-1*r*timestep)*(p*V_arr[:-1]+(1-p)*V_arr[1:])
    
    elif is_american_exercise==1:
        #American case
        for i in reversed(xrange(num_steps)):
            V_arr = exp(-1*r*timestep)*(p*V_arr[:-1]+(1-p)*V_arr[1:])
            s_t_arr = s_t_arr[:-1]/up_step
            V_arr = np.maximum(V_arr, put_adj_mult*(s_t_arr-strike))
    
    return float(V_arr[0])
    
#option Parameters
sigma = .5
r = .06
t = 1
s_price_0 = 100
close_price = 100
strike = 100
is_call = 1
is_american_exercise = 1

#model Parameters
timestep = .01

this_price = bin_price_476(s_price_0,strike,r,t,timestep,sigma,is_call,is_american_exercise)
print '{0:.2f}'.format(this_price)
    
    
    