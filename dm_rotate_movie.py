import sys

import matplotlib as mpl
mpl.use('Agg')  # for SLURM use
import matplotlib.pyplot as plt
import numpy as np
import eagle_IO.eagle_IO as E

import sphviewer as sph
from sphviewer.tools import cmaps as sph_cmaps  # custom py-sphviewer cmaps
import flaresvis

sim = '/cosma7/data/dp004/dc-love2/data/G-EAGLE/geagle_0000/data' 
tag = '012_z004p688'

N = 1080
# nrange = np.arange(0,N)
prange = np.linspace(0,360,N)

proc = int(sys.argv[1])
block = int(sys.argv[2])
nrange = np.arange(proc,N,block)

## particle properties

coods = E.read_array("SNAPSHOT", sim, tag, "/PartType1/Coordinates", numThreads=1, noH=True)

## subhalo properties

#sh_cop = E.read_array("SUBFIND", sim, tag, "/Subhalo/CentreOfPotential", numThreads=1)
#sh_mstar = E.read_array("SUBFIND", sim, tag, "/Subhalo/Stars/Mass", numThreads=1)
## hmpr = E.read_array("SUBFIND", sim, tag, "/Subhalo/HalfMassProjRad", numThreads=1)
#spin = E.read_array("SUBFIND", sim, tag, "/Subhalo/GasSpin", numThreads=1)
## sh_hmr = E.read_array("SUBFIND", sim, tag, "/Subhalo/HalfMassRad", numThreads=1)

## set centre of box

# idx = np.argsort(sh_mstar)[::-1][0]
# a,b,c = sh_cop[idx]      # use most massive (mstar) halo
a,b,c = [1600] * 3

## Align with spin axis of galaxy

# s = spin[idx]
# t = np.arctan(s[0]/s[2]) * 180./np.pi
# p = np.arctan(s[1]/s[2]) * 180./np.pi
t,p = [0] * 2

## Create part:icle and camera objects
# scaling=1
from scipy.spatial.distance import cdist
R_dist = cdist(coods, [[a,b,c]])
mask = R_dist < ((14./0.6777)-1)
mask = mask.flatten()

P = sph.Particles(coods[mask], np.ones(len(coods)))

C = sph.Camera(x=a,y=b,z=c,
               r=45,zoom=1,
               t=t,p=p,roll=0,
               xsize=4000,ysize=2250)  # 16:9


S = sph.Scene(P, Camera=C)

## loop round object
for j,p in zip(nrange, prange[nrange]):

    print("p = %s"%p)
    sys.stdout.flush()

    ## update scene camera
    S.update_camera(p=p)

    R = sph.Render(S)
    
    ## Get image and plot
    R.set_logscale()
    dm_img = R.get_image()
    dm_img = sph_cmaps.twilight()(flaresvis.get_normalized_image(dm_img,vmin=4,vmax=6.5))

    fig, ax = flaresvis.plot_img(dm_img, R.get_extent())

    fig.savefig('movie_images/dm_test_zoom_1_r_1_p_%05d.png'%j, bbox_inches='tight', pad_inches=0)

    plt.close()




