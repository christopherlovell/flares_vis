mport matplotlib.pyplot as plt
import numpy as np
import eagle as E

import sphviewer as sph
from sphviewer.tools import cmaps as sph_cmaps  # custom py-sphviewer cmaps
import vis_util
# from importlib import reload  
# reload(vis_util)

## get dark matter particles

sim = '/cosma7/data/dp004/dc-love2/data/G-EAGLE/geagle_0001/data'
tag = '014_z004p770'

coods = E.readArray("SNAPSHOT", sim, tag, "/PartType1/Coordinates", numThreads=1)

## subhalo properties

sh_cop = E.readArray("SUBFIND", sim, tag, "/Subhalo/CentreOfPotential", numThreads=1)
sh_mstar = E.readArray("SUBFIND", sim, tag, "/Subhalo/Stars/Mass", numThreads=1)
# hmpr = E.readArray("SUBFIND", sim, tag, "/Subhalo/HalfMassProjRad", numThreads=1)
spin = E.readArray("SUBFIND", sim, tag, "/Subhalo/GasSpin", numThreads=1)
# sh_hmr = E.readArray("SUBFIND", sim, tag, "/Subhalo/HalfMassRad", numThreads=1)

## set centre of box

idx = np.argsort(sh_mstar)[::-1][0]

# a,b,c = sh_com[np.argmax(hmpr[:,4])]   # use biggest galaxy (half light radius of stars)
# a,b,c = sh_com[np.argmax(sh_mstar)]      # use most massive (mstar) halo
a,b,c = sh_cop[idx]      # use most massive (mstar) halo
# a,b,c = np.mean(coods,axis=0)          # use mean of cood

## Align with spin axis of galaxy

s = spin[idx]
t = np.arctan(s[0]/s[2]) * 180./np.pi
p = np.arctan(s[1]/s[2]) * 180./np.pi


## Create particle and camera objects
scaling=1
P = sph.Particles(np.array(coods - [a,b,c]) * scaling, np.ones(len(coods)))

C = sph.Camera(x=0,y=0,z=0, 
               r=1,zoom=1,
               t=t,p=p,roll=0,
               xsize=4000,ysize=2250)  # 16:9

## Create scene and render

S = sph.Scene(P, Camera=C)
R = sph.Render(S)

## Get image and plot

R.set_logscale()
dm_img = R.get_image()

print(dm_img.min(), dm_img.max())
dm_img = sph_cmaps.night()(vis_util.get_normalized_image(dm_img,vmin=0,vmax=2.6))

fig, ax = vis_util.plot_img(dm_img, R.get_extent())

fig.savefig('images/dm_example.png', bbox_inches='tight', pad_inches=0)


