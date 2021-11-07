# -*- coding: utf-8 -*-
"""
Created on Fri Nov  5 13:40:53 2021

@author: whatf
"""

import os
import matplotlib.pyplot as plt
import numpy as np
import pandas
from iminuit import Minuit

### SPECIFY THE PATH TO THE SIMULATED DATA FILES
sim_path = "D:\Harry\Documents\Imperial\Physics\Year 4\year3-problem-solving\sim_decays\\"
###

### SET BIN NUMBER
no_of_bins = 200
###

files = os.listdir(sim_path)

data = []
figs = []
axs = []

for file in files:
    
    data.append(pandas.read_pickle(sim_path + file))
    
    figs.append(plt.figure())
    axs.append(plt.axes())
    
    axs[-1].hist(data[-1]["q2"], bins=no_of_bins, density=True)
    axs[-1].set_xlabel("$q^2$ ($GeV^2/c^4$)")
    axs[-1].set_ylabel("Probability density")
    axs[-1].set_title(file)

### SPECIFY THE PATH TO THE ACTUAL DATASET
real_path = "D:\Harry\Documents\Imperial\Physics\Year 4\year3-problem-solving\\"
real_file = "total_dataset.pkl"
###

real_data = pandas.read_pickle(real_path + real_file)
    
real_fig = plt.figure()
real_ax = plt.axes()

real_ax.hist(real_data["q2"], bins=no_of_bins, density=True)

###
real_ax.set_xlim([0,20])
real_ax.set_ylim([0, 0.1])
###

real_ax.set_xlabel("$q^2$ ($GeV^2$)")
real_ax.set_ylabel("Probability density")
real_ax.set_title(real_file)

"""
Currently, we see that 'jpsi.pkl' and 'psi2S.pkl' give expected Gaussian
lineshapes, which are easy to quantify. We also see that these two decays
dominate the background of the main dataset. So as a first step, we can fit
these decays and then try and subtract them from the main dataset. We have to
bear in mind that this might mean we lose some useful data from those q^2
ranges, but that is just the price we pay for the filtering.
"""

def Gaussian(x, mu, sigma):
    return (sigma*np.sqrt(2*np.pi))**-1 * np.exp( -(x-mu)**2 / (2*sigma**2))

jpsi_data = data[0]
psi2S_data = data[-1] #redefine these for ease of access

decays = [jpsi_data, psi2S_data]
decay_names = ["J$\psi$ $q^2$"]
mu = []
sigma = []

dec_figs = []
dec_ax = []

for decay in decays:
    vals, bins = np.histogram(decay["q2"], bins=no_of_bins, density=True)
    x = bins[:-1] + (bins[1]-bins[0])/2
    
    def LSQ(mu, sigma):
        return np.sum((vals - Gaussian(x, mu, sigma)) ** 2)
    
    m = Minuit(LSQ, mu=12, sigma=0.2,
               error_mu=0.1, error_sigma=0.01, errordef=1)
    print(m.params)
    print(m.migrad())
    
    mu.append(m.values["mu"])
    sigma.append(m.values["sigma"])
    
    dec_figs.append(plt.figure())
    dec_ax.append(plt.axes())
    
    dec_ax[-1].hist(decay["q2"], bins=no_of_bins, density=True)
    dec_ax[-1].plot(x, Gaussian(x, mu[-1], sigma[-1]))
    dec_ax[-1].set_xlabel("$q^2$ ($GeV^2/c^4$)")
    dec_ax[-1].set_ylabel("Probability density")
    dec_ax[-1].set_title(decay_names[-1])
    
    decay_names.append("$\psi2S$ $q^2$")








