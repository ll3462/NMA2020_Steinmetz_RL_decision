"""
Copied from NMA2020 tutorial
"""
import os, requests
import numpy as np
def download_all_data()
    """
    Returns
    alldat: list
        a list of dictionaries, each dictionary is data from one session
    """
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
    alldat = np.array([])
    for j in range(len(fname)):
        alldat = np.hstack((alldat, np.load('steinmetz_part%d.npz'%j, allow_pickle=True)['dat']))
    return(alldat)

def convert_spk_to_spk