# -*- coding: utf-8 -*-
"""
Created on Mon Oct 25 15:14:54 2021

@author: whatf
"""

import pandas
import matplotlib.pyplot as plt

###
fpath = "D:\Harry\Documents\Imperial\Physics\Year 4\year3-problem-solving\\"
fname = "jpsi.pkl"
###

data = pandas.read_pickle(fpath + fname)

figs = []
axs = []

for column_name in data:
    figs.append(plt.figure())
    axs.append(plt.axes())
    
    ###
    no_of_bins = 1000
    ###
    
    axs[-1].hist(data[column_name], bins=no_of_bins, density=True)
    axs[-1].set_xlabel(column_name)
    axs[-1].set_ylabel('Probability density')
    
    ###
    title = column_name + " for the $J/\psi \\rightarrow \mu\mu$ pathway"
    ###
    
    axs[-1].set_title(title)
    axs[-1].grid()
    plt.show()