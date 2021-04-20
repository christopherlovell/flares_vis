import eagle_IO.eagle_IO as E
import numpy as np
import json

import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

import flares
fl = flares.flares(fname='../../flares/data/flares.hdf5')


nthr = 8
tag = '008_z007p000'
z = float(tag[5:].replace('p','.'))
scale_factor = 1. / (1+z)

N = 10

mstar = fl.load_dataset('Mstar_30', arr_type='Galaxy')
m200 = fl.load_dataset('M200', arr_type='Galaxy')

coods = fl.load_dataset('COP', arr_type='Galaxy')
grp = fl.load_dataset('GroupNumber', arr_type='Galaxy')
sgrp = fl.load_dataset('SubGroupNumber', arr_type='Galaxy')


ind = [np.argpartition(m200[halo][tag][sgrp[halo][tag] == 0],-N)[-N:] for halo in fl.halos]

selection = np.argsort(np.hstack([m200[halo][tag][sgrp[halo][tag] == 0][_idx]\
                       [np.argsort(metric[halo][tag][sgrp[halo][tag] == 0][_idx])][::-1] \
                       for halo,_idx in zip(fl.halos,ind)]))[::-1][:N]

index = selection%N
region = (selection/N).astype(int)


out = {}
out['GroupNumber'] = [grp["%02d"%r][tag][sgrp["%02d"%r][tag] == 0][ind[r][i]].tolist() \
        for i,r in zip(index,region)]

out['SubGroupNumber'] = [sgrp["%02d"%r][tag][sgrp["%02d"%r][tag] == 0][ind[r][i]].tolist() \
        for i,r in zip(index,region)]

out['Coods'] = [(coods["%02d"%r][tag][:,sgrp["%02d"%r][tag] == 0][:,ind[r][i]] * scale_factor).tolist() \
        for i,r in zip(index,region)]

out['Mstar'] = [mstar["%02d"%r][tag][sgrp["%02d"%r][tag] == 0][ind[r][i]].tolist() \
        for i,r in zip(index,region)] 

out['M200'] = [m200["%02d"%r][tag][sgrp["%02d"%r][tag] == 0][ind[r][i]].tolist() \
        for i,r in zip(index,region)] 

out['region'] = region.tolist()


with open('selection.json','w') as fp:
    json.dump(out, fp)

