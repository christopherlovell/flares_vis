import glob
import numpy as np
import h5py

from argparse import ArgumentParser
from functools import partial

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

import schwimmbad

import sphviewer as sph
from sphviewer.tools import QuickView, cmaps


# def main(pool):

pool = schwimmbad.SerialPool() # MultiPool(processes=1)

# z = 0 snap (022)
direc = "/cosma5/data/dp004/PROJECTS/Eagle/dm_eagle_volume_L3200/snapdir_022/*.hdf5"
files = glob.glob(direc)

halo_coods = np.array([1070.13,2140.38,1498.16]) * 0.6777  ## CE-29

def read_hdf5(f,z_cood,tol=12):
    dat = np.array(h5py.File(f,'r').get('PartType1/Coordinates'))

    # filter particles by position
    mask = (dat[:,2] < (z_cood + tol)) & (dat[:,2] > (z_cood - tol))
    dat = dat[mask]
    
    if len(dat) > 0:
        return dat

lg = partial(read_hdf5, z_cood=halo_coods[2], tol=12)
p1 = list(pool.map(lg, files))
pool.close()

p1 = [p for p in p1 if p is not None]    # remove None's
p1 = np.vstack(p1)  # stack

## centre on halo
p1[:,0] += (1600*0.6777) - halo_coods[0]
mask = (p1[:,0] < 0)
p1[mask,0] += (3200 * 0.6777)
mask = (p1[:,0] > 3200*0.6777)
p1[mask,0] -= (3200 * 0.6777)

p1[:,1] += (1600*0.6777) - halo_coods[1]
mask = (p1[:,1] < 0)
p1[mask,1] += (3200 * 0.6777)
mask = (p1[:,1] > 3200*0.6777)
p1[mask,1] -= (3200 * 0.6777)

p1 /= 0.6777     # comoving h-less

res=5000 # number of pixels in image
centre = 3200 / 2

# P = sph.Particles(p1[:,[2,1,0]],mass=np.ones(len(p1)))
h = np.ones(len(p1)) 
P = sph.Particles(p1,mass=np.ones(len(p1)),hsml=h)


for i in np.arange(426,640):
    print(i)
    # i = 300
    dl = (3200-(i*5)) / 2
    convers = res/(2*dl) # conversion factor
    
    ## Start figure ##
    fig,ax = plt.subplots(1,1,figsize=(10,10))
    
    C = sph.Camera(r='infinity',t=0,p=0,roll=0, xsize=res, ysize=res,
                   x=centre,y=centre,z=halo_coods[2] / 0.6777,extent=[-dl,dl,-dl,dl])
    
    S = sph.Scene(P,C)
    R = sph.Render(S)
    extent = R.get_extent()
    lpixel  = (extent[1]-extent[0])/float(res)

    img = np.log10(R.get_image())
    
    ax.imshow(img-np.log10(lpixel**2),cmap=cmaps.twilight(),vmin=0.25,vmax=3.9)
    
    ax.xaxis.set_major_formatter(FuncFormatter(lambda x, pos: x/convers))
    ax.yaxis.set_major_formatter(FuncFormatter(lambda x, pos: x/convers))
    ax.set_xlabel('$\mathrm{Mpc}$',size=15)
    ax.set_ylabel('$\mathrm{Mpc}$',size=15)
     
    fig.savefig('plots/parent_zoom/parent_zoom_%s.png'%i, dpi=299)
    # fig.show()
    



# if __name__ == '__main__':
# 
#     parser = ArgumentParser(description="Schwimmbad example.")
# 
#     group = parser.add_mutually_exclusive_group()
#     group.add_argument("--ncores", dest="n_cores", default=1,
#                        type=int, help="Number of processes (uses multiprocessing).")
#     group.add_argument("--mpi", dest="mpi", default=False,
#                        action="store_true", help="Run with MPI.")
#     args = parser.parse_args()
# 
#     pool = schwimmbad.choose_pool(mpi=args.mpi, processes=args.n_cores)
#     print(pool)
#     main(pool)
# 
#     print("All done. Spec-tacular!")

