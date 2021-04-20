import eagle_IO.eagle_IO as E
import numpy as np
import json

import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

import flares
fl = flares.flares(fname='../../flares/data/flares.hdf5')


nthr = 8
direc = '/cosma7/data/dp004/dc-love2/data/G-EAGLE/geagle_0000/data'
tag = '008_z007p000'
z = float(tag[5:].replace('p','.'))
scale_factor = 1. / (1+z)

N = 10

mstar = fl.load_dataset('Mstar_30', arr_type='Galaxy')
m200 = fl.load_dataset('M200', arr_type='Galaxy')

coods = fl.load_dataset('COP', arr_type='Galaxy')
grp = fl.load_dataset('GroupNumber', arr_type='Galaxy')
sgrp = fl.load_dataset('SubGroupNumber', arr_type='Galaxy')

metric = m200

ind = [np.argpartition(metric[halo][tag],-N)[-N:] for halo in fl.halos]

selection = np.argsort(np.hstack([metric[halo][tag][_idx][np.argsort(metric[halo][tag][_idx])][::-1] \
                       for halo,_idx in zip(fl.halos,ind)]))[::-1][:N]

index = selection%N
region = (selection/N).astype(int)


out = {}
out['GroupNumber'] = [grp["%02d"%r][tag][ind[r][i]].tolist() for i,r in zip(index,region)]
out['SubGroupNumber'] = [sgrp["%02d"%r][tag][ind[r][i]].tolist() for i,r in zip(index,region)]
out['Coods'] = [(coods["%02d"%r][tag][:,ind[r][i]] * scale_factor).tolist() for i,r in zip(index,region)]
out['Mstar'] = [mstar["%02d"%r][tag][ind[r][i]].tolist() for i,r in zip(index,region)] 
out['M200'] = [m200["%02d"%r][tag][ind[r][i]].tolist() for i,r in zip(index,region)] 
out['region'] = region.tolist()


with open('selection.json','w') as fp:
    json.dump(out, fp)

