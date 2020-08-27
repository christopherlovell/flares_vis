import sys
import numpy as np
import h5py

import matplotlib as mpl
import matplotlib.patches as patches
import matplotlib.pyplot as plt
mpl.use('Agg')
# mpl.rcParams['savefig.pad_inches'] = 0

import sphviewer as sph
from sphviewer.tools import cmaps


def read_hdf5(f,z_cood,tol=12):
    print("Loading",f)
    sys.stdout.flush()

    dat = np.array(h5py.File(f,'r').get('PartType1/Coordinates'))

    # filter particles by position
    mask = (dat[:,2] < (z_cood + tol)) & (dat[:,2] > (z_cood - tol))
    dat = dat[mask]

    print(f,"complete!")
    sys.stdout.flush()

    if len(dat) > 0:
        return dat
    else:
        return None


def modified_sigmoid(x,k):
    if x == 0:
        return 0.
    else:
        return 1 - (1 / (1 + (1./x - 1)**-k) )


def plot_parent(i,P,n,res,centre,z_centre):
    print("i:",i); sys.stdout.flush()
    cmap = cmaps.twilight()
    
    f = modified_sigmoid(i/n,3)
    L,l = 3300/2,50
    dl = L*(1-f) + l*f
    R = 16./9
    offset = 100
    dx = dl*R
    dy = dl

    ext_x = 3200/2
    ext_y = 3200/2
    if ext_x > dx: ext_x = dx
    if ext_y > dy: ext_y = dy 

    C = sph.Camera(r='infinity', t=0, p=0, roll=0, xsize=res, ysize=res,
                   x=centre,y=centre,z=z_centre,extent=[-ext_x,ext_x,-ext_y,ext_y])

    S = sph.Scene(P,C)
    R = sph.Render(S)
    extent = R.get_extent()
    img = np.log10(R.get_image())
    print(img.max(),img.min())

    fig = plt.figure(figsize=(16,9))
    ax = fig.add_axes([0,0,1,1])
    
    # ax.imshow(img, cmap=cmap, vmin=-0.05, vmax=1.2, extent=extent,aspect='equal')
    ax.imshow(img, cmap=cmap, vmin=--1, vmax=2.4, extent=extent,aspect='equal')

    del(img); del(C); 

    ax.set_facecolor(cmap(0.0))
    ax.set_xlim(-dx,dx)
    ax.set_ylim(-dy,dy)
    
    ax.hlines(0.9, 0.092, 0.192, transform=ax.transAxes, 
              color='red', lw=2)
    ax.text(0.1, 0.94, '$%i \; \mathrm{cMpc}$'%(dx*0.2), 
            transform=ax.transAxes, size=12, color='black')

    rect = patches.Rectangle((0.09,0.92),0.105,0.065, 
                              linewidth=1,edgecolor='none', 
                              facecolor='white',alpha=0.5, 
                              transform=ax.transAxes)

    ax.add_patch(rect) 

    ax.get_xaxis().set_visible(False)
    ax.get_yaxis().set_visible(False)

    # plt.show()
    fname = 'plots/parent_zoom/parent_zoom_%03d.png'%i
    # plt.gca().set_axis_off()
    # plt.subplots_adjust(top = 1, bottom = 0, right = 1, left = 0, 
    #                     hspace = 0, wspace = 0)
    # plt.margins(0,0)
    print(fname)
    fig.savefig(fname, dpi=150)#, bbox_inches='tight', pad_inches = 0)
    plt.close(fig)
