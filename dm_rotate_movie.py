import sys

import matplotlib as mpl
mpl.use('Agg')  # for SLURM use
import matplotlib.pyplot as plt
import numpy as np
import eagle as E

import sphviewer as sph
from sphviewer.tools import cmaps as sph_cmaps  # custom py-sphviewer cmaps
import vis_util
# from importlib import reload  
# reload(vis_util)

sim = '/cosma7/data/dp004/dc-love2/data/G-EAGLE/geagle_0000/data' 
tag = '014_z004p770'

## get input
if len(sys.argv) > 1:
    n1 = int(sys.argv[1])
    n2 = int(sys.argv[2])
    nrange = np.arange(n1,n2)
else:
    nrange = np.arange(0,360)

## particle properties

coods = E.readArray("SNAPSHOT", sim, tag, "/PartType1/Coordinates", numThreads=1)

## subhalo properties

sh_cop = E.readArray("SUBFIND", sim, tag, "/Subhalo/CentreOfPotential", numThreads=1)
sh_mstar = E.readArray("SUBFIND", sim, tag, "/Subhalo/Stars/Mass", numThreads=1)
# hmpr = E.readArray("SUBFIND", sim, tag, "/Subhalo/HalfMassProjRad", numThreads=1)
spin = E.readArray("SUBFIND", sim, tag, "/Subhalo/GasSpin", numThreads=1)
# sh_hmr = E.readArray("SUBFIND", sim, tag, "/Subhalo/HalfMassRad", numThreads=1)

## set centre of box

idx = np.argsort(sh_mstar)[::-1][0]
a,b,c = sh_cop[idx]      # use most massive (mstar) halo

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


S = sph.Scene(P, Camera=C)

## loop round object
for i in nrange:

    print("p = %s"%i)
    sys.stdout.flush()

    ## update scene camera
    S.update_camera(p=i)

    R = sph.Render(S)
    
    ## Get image and plot
    R.set_logscale()
    dm_img = R.get_image()
    dm_img = sph_cmaps.night()(vis_util.get_normalized_image(dm_img,vmin=0,vmax=2.6))

    fig, ax = vis_util.plot_img(dm_img, R.get_extent())

    fig.savefig('movie_images/dm_test_zoom_1_r_1_p_%03d.png'% i, bbox_inches='tight', pad_inches=0)

    plt.close()




