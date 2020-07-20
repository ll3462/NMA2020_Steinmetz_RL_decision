# -*- coding: utf-8 -*-
"""
Created on Mon Jul 20 11:06:46 2020

@author: tang_
"""
#%%
#@title Data retrieval
import os, requests

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
import numpy as np
import matplotlib.pyplot as plt
alldat = np.array([])
for j in range(len(fname)):
  alldat = np.hstack((alldat, np.load('steinmetz_part%d.npz'%j, allow_pickle=True)['dat']))

# select just one of the recordings here. 11 is nice because it has some neurons in vis ctx. 
dat = alldat[11]
print(dat.keys())
#%% summary plot of all sessions
Ctrst_right_allSession=[]
Ctrst_left_allSession=[]
Responses_allSession=[]
Feedbacks_allSession=[]

for n_dat in range(len(alldat)):
#for n_dat in [1,2]:
    dat = alldat[n_dat]
    Ctrst_right=dat['contrast_right']
    Ctrst_left=dat['contrast_left']
    Responses=dat['response']
    Feedbacks = dat['feedback_type']
    Ctrst_right_allSession=np.hstack((Ctrst_right_allSession,Ctrst_right))
    Ctrst_left_allSession=np.hstack((Ctrst_left_allSession,Ctrst_left))
    Responses_allSession=np.hstack((Responses_allSession,Responses))
    Feedbacks_allSession=np.hstack((Feedbacks_allSession,Feedbacks))
#    Ctrst_right_allSession=[]
#    Ctrst_left_allSession=[]
#    Responses_allSession=[]
#    Feedbacks_allSession=[]
#    Ctrst_right_allSession=Ctrst_right
#    Ctrst_left_allSession=Ctrst_left
#    Responses_allSession=Responses
#    Feedbacks_allSession=Feedbacks
#%%
#all datasets combined
C_right_all = np.unique(Ctrst_right_allSession)
C_left_all = np.unique(Ctrst_left_allSession)
Ctrst_delta = Ctrst_right_allSession-Ctrst_left_allSession
uni_Ctrst_delta = np.unique(Ctrst_delta)

frac_resp_d = np.ones([len(uni_Ctrst_delta),1])
for c_d in range(len(uni_Ctrst_delta)):
  Idx_c_d = Ctrst_delta==uni_Ctrst_delta[c_d]
  response_all = Responses_allSession[Idx_c_d]
  frac_resp_d[c_d] = np.sum(response_all==1)/(np.sum(response_all==1)+np.sum(response_all==-1))
  
#fig = plt.figure(figsize=(15.0, 5.0))
#ax1 = fig.add_subplot(1, 3, 1)
#plt.plot(uni_Ctrst_delta,frac_resp_d,'ko')
#plt.show()
#%%last trial contrast &with reward

Ctrst_delta_last = Ctrst_delta[1:,]
Ctrst_delta_current = Ctrst_delta[:-1,]
resp_last =Responses_allSession[1:,]
resp_current =Responses_allSession[:-1,]
Feedbacks_last = Feedbacks_allSession[1:,]

frac_resp = np.ones([len(uni_Ctrst_delta),len(uni_Ctrst_delta)])

for i_ctrst_last in range(len(uni_Ctrst_delta)):
    Idx_ctrst_last = Ctrst_delta_last==uni_Ctrst_delta[i_ctrst_last]
    Idx_last_posi = Feedbacks_last!=0
    Idx_last = np.logical_and(Idx_ctrst_last,Idx_last_posi)
    for i_ctrst_curr in range(len(uni_Ctrst_delta)):
        Idx_curr = Ctrst_delta_current==uni_Ctrst_delta[i_ctrst_curr]
        i_resp=resp_current[np.logical_and(Idx_last,Idx_curr)]
        frac_resp[i_ctrst_last,i_ctrst_curr]=np.sum(i_resp==1)/(np.sum(i_resp==1)+np.sum(i_resp==-1))

fig = plt.figure(figsize=(15.0, 5.0))
ax2 = fig.add_subplot(1, 3, 2)
#plt.colorbar
pt2=plt.imshow(frac_resp.T)
plt.xlabel('previous cue')
plt.ylabel('current cue')
plt.xticks(ticks=[0,4,8],labels=['-1','0','1'])
plt.yticks(ticks=[0,4,8],labels=['-1','0','1'])
plt.colorbar(pt2)

#plt.show()

#%% last trial reward
    
frac_resp_sum = np.ones([len(uni_Ctrst_delta),len(uni_Ctrst_delta)])

for i_ctrst_last in range(len(uni_Ctrst_delta)):
    Idx_ctrst_last = Ctrst_delta_last==uni_Ctrst_delta[i_ctrst_last]
    Idx_last_posi = Feedbacks_last!=0
#    Idx_last_posi = Feedbacks_last==1
    Idx_last=Idx_last_posi
#    Idx_last = np.logical_and(Idx_ctrst_last,Idx_last_posi)
    for i_ctrst_curr in range(len(uni_Ctrst_delta)):
        Idx_curr = Ctrst_delta_current==uni_Ctrst_delta[i_ctrst_curr]
        i_resp=resp_current[np.logical_and(Idx_last,Idx_curr)]
        frac_resp_sum[i_ctrst_last,i_ctrst_curr]=np.sum(i_resp==1)/(np.sum(i_resp==1)+np.sum(i_resp==-1))

#fig = plt.figure(figsize=(15.0, 5.0))
ax1 = fig.add_subplot(1, 3, 1)
pt1=plt.imshow(frac_resp_sum.T)
plt.xlabel('previous reward trial')
plt.ylabel('current cue')
plt.xticks(ticks=[0,4,8],labels=['-1','0','1'])
plt.yticks(ticks=[0,4,8],labels=['-1','0','1'])#plt.show()
plt.colorbar(pt1)
plt.title('all session')


#%% plot updating
#fig = plt.figure(figsize=(10.0, 10.0))
ax3 = fig.add_subplot(1, 3, 3)
pt3=plt.imshow(frac_resp.T-frac_resp_sum.T,vmax=0.2,vmin=-0.2)
plt.xlabel('previous cue')
plt.ylabel('current cue')
plt.xticks(ticks=[0,4,8],labels=['-1','0','1'])
plt.yticks(ticks=[0,4,8],labels=['-1','0','1'])
plt.colorbar(pt3)
plt.show()
fig.savefig('all_session.png')
#%%plot individual session
for n_dat in range(len(alldat)):
#for n_dat in [1,2]:
    dat = alldat[n_dat]
    Ctrst_right=dat['contrast_right']
    Ctrst_left=dat['contrast_left']
    Responses=dat['response']
    Feedbacks = dat['feedback_type']
    
    #%%
    #all datasets combined
    C_right_all = np.unique(Ctrst_right)
    C_left_all = np.unique(Ctrst_left)
    Ctrst_delta = Ctrst_right-Ctrst_left
    uni_Ctrst_delta = np.unique(Ctrst_delta)
    
    frac_resp_d = np.ones([len(uni_Ctrst_delta),1])
    for c_d in range(len(uni_Ctrst_delta)):
      Idx_c_d = Ctrst_delta==uni_Ctrst_delta[c_d]
      response_all = Responses[Idx_c_d]
      frac_resp_d[c_d] = np.sum(response_all==1)/(np.sum(response_all==1)+np.sum(response_all==-1))
      
    #fig = plt.figure(figsize=(15.0, 5.0))
    #ax1 = fig.add_subplot(1, 3, 1)
    #plt.plot(uni_Ctrst_delta,frac_resp_d,'ko')
    #plt.show()
    #%%last trial contrast &with reward
    
    Ctrst_delta_last = Ctrst_delta[1:,]
    Ctrst_delta_current = Ctrst_delta[:-1,]
    resp_last =Responses[1:,]
    resp_current =Responses[:-1,]
    Feedbacks_last = Feedbacks[1:,]
    
    frac_resp = np.ones([len(uni_Ctrst_delta),len(uni_Ctrst_delta)])
    
    for i_ctrst_last in range(len(uni_Ctrst_delta)):
        Idx_ctrst_last = Ctrst_delta_last==uni_Ctrst_delta[i_ctrst_last]
        Idx_last_posi = Feedbacks_last!=0
        Idx_last = np.logical_and(Idx_ctrst_last,Idx_last_posi)
        for i_ctrst_curr in range(len(uni_Ctrst_delta)):
            Idx_curr = Ctrst_delta_current==uni_Ctrst_delta[i_ctrst_curr]
            i_resp=resp_current[np.logical_and(Idx_last,Idx_curr)]
            frac_resp[i_ctrst_last,i_ctrst_curr]=np.sum(i_resp==1)/(np.sum(i_resp==1)+np.sum(i_resp==-1))
    
    fig = plt.figure(figsize=(15.0, 5.0))
    ax2 = fig.add_subplot(1, 3, 2)
    #plt.colorbar
    pt2=plt.imshow(frac_resp.T)
    plt.xlabel('previous cue')
    plt.ylabel('current cue')
    plt.xticks(ticks=[0,4,8],labels=['-1','0','1'])
    plt.yticks(ticks=[0,4,8],labels=['-1','0','1'])
    plt.colorbar(pt2)
    
    #plt.show()
    
    #%% last trial reward
        
    frac_resp_sum = np.ones([len(uni_Ctrst_delta),len(uni_Ctrst_delta)])
    
    for i_ctrst_last in range(len(uni_Ctrst_delta)):
        Idx_ctrst_last = Ctrst_delta_last==uni_Ctrst_delta[i_ctrst_last]
        Idx_last_posi = Feedbacks_last!=0
    #    Idx_last_posi = Feedbacks_last==1
        Idx_last=Idx_last_posi
    #    Idx_last = np.logical_and(Idx_ctrst_last,Idx_last_posi)
        for i_ctrst_curr in range(len(uni_Ctrst_delta)):
            Idx_curr = Ctrst_delta_current==uni_Ctrst_delta[i_ctrst_curr]
            i_resp=resp_current[np.logical_and(Idx_last,Idx_curr)]
            frac_resp_sum[i_ctrst_last,i_ctrst_curr]=np.sum(i_resp==1)/(np.sum(i_resp==1)+np.sum(i_resp==-1))
    
    #fig = plt.figure(figsize=(15.0, 5.0))
    ax1 = fig.add_subplot(1, 3, 1)
    pt1=plt.imshow(frac_resp_sum.T)
    plt.xlabel('previous reward trial')
    plt.ylabel('current cue')
    plt.xticks(ticks=[0,4,8],labels=['-1','0','1'])
    plt.yticks(ticks=[0,4,8],labels=['-1','0','1'])#plt.show()
    plt.colorbar(pt1)
    plt.title('session '+ str(n_dat))
    
    #%% plot updating
    #fig = plt.figure(figsize=(10.0, 10.0))
    ax3 = fig.add_subplot(1, 3, 3)
    pt3=plt.imshow(frac_resp.T-frac_resp_sum.T,vmax=0.2,vmin=-0.2)
    plt.xlabel('previous cue')
    plt.ylabel('current cue')
    plt.xticks(ticks=[0,4,8],labels=['-1','0','1'])
    plt.yticks(ticks=[0,4,8],labels=['-1','0','1'])
    plt.colorbar(pt3)
    plt.show()
    fig.savefig('all_session_'+str(n_dat) +'.png')
    
