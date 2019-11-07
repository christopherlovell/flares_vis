import numpy as np
import h5py

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

import sphviewer as sph
from sphviewer.tools import cmaps


def read_hdf5(f,z_cood,tol=12):
    dat = np.array(h5py.File(f,'r').get('PartType1/Coordinates'))

    # filter particles by position
    mask = (dat[:,2] < (z_cood + tol)) & (dat[:,2] > (z_cood - tol))
    dat = dat[mask]

    if len(dat) > 0:
        return dat




def plot_parent(i,dl,res,centre,z_centre):
    dl = (3200-(i*5)) / 2
    convers = res/(2*dl) # conversion factor

    ## Start figure ##
    fig,ax = plt.subplots(1,1,figsize=(10,10))

    C = sph.Camera(r='infinity',t=0,p=0,roll=0, xsize=res, ysize=res,
                   x=centre,y=centre,z=z_centre,extent=[-dl,dl,-dl,dl])

    S = sph.Scene(P,C)
    R = sph.Render(S)
    extent = R.get_extent()
    lpixel  = (extent[1]-extent[0])/float(res)

    img = np.log10(R.get_image())

    ax.imshow(img-np.log10(lpixel**2),cmap=cmaps.twilight(),vmin=0.25,vmax=3.9)

    # ax.xaxis.set_major_formatter(FuncFormatter(lambda x, pos: x/convers))
    # ax.yaxis.set_major_formatter(FuncFormatter(lambda x, pos: x/convers))
    # ax.set_xlabel('$\mathrm{Mpc}$',size=15)
    # ax.set_ylabel('$\mathrm{Mpc}$',size=15)

    fig.savefig('plots/parent_zoom/parent_zoom_%s.png'%i, dpi=299)
    # fig.show()
    # plt.show()
    plt.close(fig)

