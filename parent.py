import glob
import numpy as np
import h5py

from argparse import ArgumentParser
from functools import partial

## ! if running as a job, use 'Agg' backend
import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

import schwimmbad

import sphviewer as sph
from sphviewer.tools import QuickView, cmaps

from _parent import read_hdf5, plot_parent


# pool = schwimmbad.MultiPool(processes=1)
# 
# # z = 0 snap (022)
# direc = "/cosma5/data/dp004/PROJECTS/Eagle/dm_eagle_volume_L3200/snapdir_022/*.hdf5"
# files = glob.glob(direc)
# print("N(files):",len(files))
# 
# halo_coods = np.array([1070.13,2140.38,1498.16]) * 0.6777  ## CE-29
# 
# print("Reading source HDF5...")
# lg = partial(read_hdf5, z_cood=halo_coods[2], tol=10)
# p1 = list(pool.map(lg, files))
# pool.close()
# 
# print("Tidying and centering..")
# p1 = [p for p in p1 if p is not None]    # remove None's
# p1 = np.vstack(p1)  # stack
# 
# ## centre on halo
# p1[:,0] += (1600*0.6777) - halo_coods[0]
# mask = (p1[:,0] < 0)
# p1[mask,0] += (3200 * 0.6777)
# mask = (p1[:,0] > 3200*0.6777)
# p1[mask,0] -= (3200 * 0.6777)
# 
# p1[:,1] += (1600*0.6777) - halo_coods[1]
# mask = (p1[:,1] < 0)
# p1[mask,1] += (3200 * 0.6777)
# mask = (p1[:,1] > 3200*0.6777)
# p1[mask,1] -= (3200 * 0.6777)
# 
# p1 /= 0.6777     # comoving h-less

# np.savetxt("dm_particles.txt",p1)
p1 = np.loadtxt("dm_particles.txt")

res=5000 # number of pixels in image
centre = 3200 / 2

print("Creating particles...")
# P = sph.Particles(p1[:,[2,1,0]],mass=np.ones(len(p1)))
h = np.ones(len(p1)) * 0.5 
P = sph.Particles(p1,mass=np.ones(len(p1)),hsml=h)
N = 630 # number of images

print("Creating images...")
for i in np.arange(N):
    print(i)
    plot_parent(i,P=P,n=N,res=res,centre=centre,
                z_centre=halo_coods[2]/0.6777)

# pool = schwimmbad.MultiPool(processes=8)
# 
# lg = partial(plot_parent, P=P, n=N, res=res, centre=centre,
#              z_centre=halo_coods[2]/0.6777)
# 
# pool.map(lg, np.arange(N))
# pool.close()

