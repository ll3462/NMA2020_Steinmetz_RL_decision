# -*- coding: utf-8 -*-
"""
Created on Thu Jul 23 13:37:25 2020

@author: tang_
"""
#%%
import os, requests
import numpy as np
import matplotlib.pyplot as plt
from scipy import io

#%%
#@title Data retrieval

fname = []
for j in range(3):
  fname.append('steinmetz_part%d.npz'%j)
url = ["https://osf.io/agvxh/download"]
url.append("https://osf.io/uv3mw/download")
url.append("https://osf.io/ehmw2/download")

for j in range(len(url)):
  if not os.path.isfile(fname[j]):
    try:
      r = requests.get(url[j])
    except requests.ConnectionError:
      print("!!! Failed to download data !!!")
    else:
      if r.status_code != requests.codes.ok:
        print("!!! Failed to download data !!!")
      else:
        with open(fname[j], "wb") as fid:
          fid.write(r.content)
#%%
#@title Data loading

alldat = np.array([])
for j in range(len(fname)):
  alldat = np.hstack((alldat, np.load('steinmetz_part%d.npz'%j, allow_pickle=True)['dat']))

# select just one of the recordings here. 11 is nice because it has some neurons in vis ctx. 
dat = alldat[11]
print(dat.keys())
#%%
#import neo
#import quantities as pq
#from elephant.spike_train_generation import inhomogeneous_poisson_process

#spks=dat['spks']
    
def formating(alldat,sessionIdx=11):
    dat = alldat[sessionIdx]
    spks=dat['spks']
    bin_size=dat['bin_size']
    t_idx= np.linspace(bin_size/2,bin_size*(spks.shape[2]+0.5),num=spks.shape[2],endpoint=False)
    
    spiketrains=[]
    for n_trial in range(spks.shape[1]):
        trial_spks=spks[:,n_trial,:]
        spkstrain=[]
        for n_neuron in range(spks.shape[0]):
            neuron_spks=trial_spks[n_neuron,:]
            neuron_spksT=t_idx[neuron_spks==1]
            spkstrain.append(neuron_spksT)
        spiketrains.append(spkstrain)
    
    return spiketrains

    
#%%
spks=np.load('spks.npy')
response=np.load('response.npy')
brain_area=np.load('brain_area.npy')
bin_size=np.load('bin_size.npy')
spiketrains=formating(alldat,sessionIdx=11)


io.savemat('spiketrains.mat',{'spiketrains':spiketrains})
io.savemat('spks.mat',{'spks':spks})
io.savemat('response.mat',{'response':response})
io.savemat('brain_area.mat',{'brain_area':brain_area})
io.savemat('bin_size.mat',{'bin_size':bin_size})


        









