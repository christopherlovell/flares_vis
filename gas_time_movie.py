import matplotlib as mpl
mpl.use('Agg')  # for SLURM use
import matplotlib.pyplot as plt
import numpy as np
import eagle as E
import sys

import sphviewer as sph
from sphviewer.tools import cmaps as sph_cmaps  # custom py-sphviewer cmaps
import vis_util

## get input
if len(sys.argv) > 1:
    tag_idx = int(sys.argv[1])
else:
    tag_idx = 14

sim = '/cosma7/data/dp004/dc-love2/data/G-EAGLE/geagle_0000/data' 
tags = ['000_z015p048','001_z012p762','002_z011p146','003_z009p934',
        '004_z008p985','005_z008p218','006_z007p583','007_z007p047',
        '008_z006p587','009_z006p188','010_z005p837','011_z005p526',
        '012_z005p248','013_z004p997','014_z004p770']#,'015_z004p688']

tag = tags[tag_idx]

## particle properties

coods = E.readArray("SNAPSHOT", sim, tag, "/PartType0/Coordinates", numThreads=1, physicalUnits=False)
pmass = E.readArray("SNAPSHOT", sim, tag, "/PartType0/Mass", numThreads=1, physicalUnits=False)
ptemp = E.readArray("SNAPSHOT", sim, tag, "/PartType0/Temperature", numThreads=1, physicalUnits=False)
# phsml = E.readArray("SNAPSHOT", sim, tag, "/PartType0/SmoothingLength", numThreads=1, physicalUnits=False)

## subhalo properties

sh_cop = E.readArray("SUBFIND", sim, tag, "/Subhalo/CentreOfPotential", numThreads=1, physicalUnits=False)
sh_mstar = E.readArray("SUBFIND", sim, tag, "/Subhalo/Stars/Mass", numThreads=1, physicalUnits=False)
spin = E.readArray("SUBFIND", sim, tag, "/Subhalo/GasSpin", numThreads=1, physicalUnits=False)

## set centre of box

idx = np.argsort(sh_mstar)[::-1][0]
a,b,c = sh_cop[idx]      # use most massive (mstar) halo

## Align with spin axis of galaxy

# s = spin[idx]
t = 0 #np.arctan(s[0]/s[2]) * 180./np.pi
p = 0 #np.arctan(s[1]/s[2]) * 180./np.pi

## Create particle and camera objects

dx = 3
norm_coods = coods - [a,b,c]
coods_mask = (norm_coods[:,0] < dx) & (norm_coods[:,0] > -dx) &\
             (norm_coods[:,1] < dx) & (norm_coods[:,1] > -dx) &\
             (norm_coods[:,2] < dx) & (norm_coods[:,2] > -dx)

C = sph.Camera(x=0,y=0,z=0,r='infinity',extent=[-dx,dx,-dx,dx],
               t=t,p=p,roll=0,xsize=4000,ysize=2250)

# Gas density
P = sph.Particles(norm_coods[coods_mask], 
                  pmass[coods_mask] / pmass[coods_mask].min())
                  # hsml = hsml * 10)# * 2)

hsml = P.get_hsml()

## Create scene and render
S = sph.Scene(P, Camera=C)
R = sph.Render(S)

## Get image and plot
# R.set_logscale()
img = R.get_image()
print(img.min(), img.max())

cmap = sph_cmaps.desert() # plt.get_cmap('twilight')
img = cmap(vis_util.get_normalized_image(img,vmin=0,vmax=7))

fig, ax = vis_util.plot_img(img, R.get_extent())
# plt.show()
fig.savefig('test_out/gas_time_%s.png'%(tag_idx), bbox_inches='tight', pad_inches=0)


