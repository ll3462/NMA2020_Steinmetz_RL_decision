# -*- coding: utf-8 -*-
"""
Created on Thu Jul 23 10:04:43 2020

@author: tang_
"""
#%%
import os, requests
import numpy as np
import matplotlib.pyplot as plt
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
#%% list of all the recorded brain areas
UNI_brain_area=np.unique(dat['brain_area'])
for i in range(alldat.shape[0]):
    dat = alldat[i]
    brain_areas=dat['brain_area']
    uni_brain_area=np.unique(brain_areas)
    UNI_brain_area=np.unique(np.hstack((uni_brain_area,UNI_brain_area)))
#%% count neuron number in each brain areas of each recording session
Counts_neuro = np.zeros((alldat.shape[0],UNI_brain_area.shape[0]))
for i in range(alldat.shape[0]):
    dat = alldat[i]
    brain_areas=dat['brain_area']
    for nn in range(len(UNI_brain_area)):
        Counts_neuro[i,nn]=np.sum(brain_areas==UNI_brain_area[nn])
Counts_neuro_nn=Counts_neuro[:,:-1]
fig = plt.figure(figsize=(6.0, 10.0),dpi=100)
#plt.imshow(Counts_neuro_nn.T,vmax=20)
plt.imshow(Counts_neuro_nn.T>=5)
plt.xlabel('session')
plt.ylabel('areas')
plt.yticks(ticks=range(len(UNI_brain_area)),labels=UNI_brain_area,rotation=0)
#plt.colorbar()
#fig.savefig('brainAreas_all_session.png')
fig.savefig('brainAreas_all_session_N5plus.png')

    
    
    
    
