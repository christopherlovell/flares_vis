import glob
import numpy as np

import schwimmbad
from functools import partial

import sphviewer as sph




from _parent import read_hdf5, plot_parent

# halo_coods = np.array([1070.13,2140.38,1498.16]) * 0.6777  ## CE-29
halo_coods = np.array([623.48, 1142.15, 1525.28]) #* 0.6777  ## FLARES-00

# pool = schwimmbad.MultiPool(processes=8)
# 
# # z = 0, snap 022
# # direc = "/cosma5/data/dp004/PROJECTS/Eagle/dm_eagle_volume_L3200/snapdir_022/*.hdf5"
# # z = 4.67, snap 002
# direc = "/cosma5/data/dp004/PROJECTS/Eagle/dm_eagle_volume_L3200/snapdir_002/*.hdf5"
# 
# files = glob.glob(direc)
# print("N(files):",len(files))
#  
# print("Reading source HDF5...")
# lg = partial(read_hdf5, z_cood=halo_coods[2], tol=22)
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
# 
# np.save('dm_particles.npy',p1)
# 
# # reduce particle number
# print("len(P):",len(p1))
# pmask = np.random.rand(len(p1)) < 0.95
# print("len(P[mask]):",np.sum(pmask))
# 
# p1 = p1[pmask]
# np.save('dm_particles_small.npy',p1)
# 
# p1 = np.load('dm_particles_small.npy')
p1 = np.load('dm_particles.npy')
pmask = np.random.rand(len(p1)) < 0.95
print("len(P[mask]):",np.sum(pmask))
p1 = p1[pmask]

res=5000 # number of pixels in image
centre = 3200 / 2

print("Creating particles...")
# P = sph.Particles(p1[:,[2,1,0]],mass=np.ones(len(p1)))
# h = np.ones(len(p1)) * 0.5 
P = sph.Particles(p1,mass=np.ones(len(p1)))#,hsml=h)
N = 720 # number of images

print("Creating images...")
# for i in np.arange(N):
#     print(i)
i = 0
plot_parent(i,P=P,n=N,res=res,centre=centre,
            z_centre=halo_coods[2]/0.6777)

# pool = schwimmbad.MultiPool(processes=16)
# 
# lg = partial(plot_parent, P=P, n=N, res=res, centre=centre,
#              z_centre=halo_coods[2]/0.6777)
# 
# pool.map(lg, np.arange(N))
# pool.close()

