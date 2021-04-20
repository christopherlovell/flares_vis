import numpy as np
import json

import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
import matplotlib.patches as patches

import sphviewer as sph
from sphviewer.tools import QuickView, cmaps

import eagle_IO.eagle_IO as E
import flares
fl = flares.flares(fname='../../flares/data/flares.hdf5')

mstar = fl.load_dataset('Mstar_30', arr_type='Galaxy')
grp = fl.load_dataset('GroupNumber', arr_type='Galaxy')
sgrp = fl.load_dataset('SubGroupNumber', arr_type='Galaxy')


with open('selection.json','r') as fp:
    selection = json.load(fp)


nthr = 8
tag = '008_z007p000'


for region in np.unique(selection['region']):
    print("Region:",region)

    direc = '/cosma7/data/dp004/dc-love2/data/G-EAGLE/geagle_%04d/data'%int(region)
    
    pgas = E.read_array("SNAPSHOT", direc, tag, "/PartType0/Coordinates", 
                        numThreads=nthr, noH=True, physicalUnits=True)

    for i in np.where(np.array(selection['region']) == region)[0]:
        print("Galaxy:",i)
        c = np.array(selection['Coods'])[i]

        _idx = np.where((grp["%02d"%region][tag] == np.array(selection['GroupNumber'])[i]) & \
                        (sgrp["%02d"%region][tag] == np.array(selection['SubGroupNumber'])[i]))[0]

        dl = 0.02
        pmask = (pgas[:,0] > c[0]-dl)
        pmask[pmask] = (pgas[pmask,0] < c[0]+dl)
        pmask[pmask] = (pgas[pmask,1] > c[1]-dl)
        pmask[pmask] = (pgas[pmask,1] < c[1]+dl)
        pmask[pmask] = (pgas[pmask,2] > c[2]-dl)
        pmask[pmask] = (pgas[pmask,2] < c[2]+dl)

        # pmask = ((pgas[:,0] > coods[0]-dl) & (pgas[:,0] < coods[0]+dl) &\
        #          (pgas[:,1] > coods[1]-dl) & (pgas[:,1] < coods[1]+dl) &\
        #          (pgas[:,2] > coods[2]-dl) & (pgas[:,2] < coods[2]+dl))
        
        print(len(pgas),np.sum(pmask))
        if np.sum(pmask) == 0:
            raise ValueError('No particles to plot')

        ext=500 # number of pixels in image
        convers = ext/(2*dl) # conversion factor
        
        P = sph.Particles(pgas[pmask],mass=np.ones(np.sum(pmask)))
        
        fig,(ax1,ax2,ax3) = plt.subplots(1,3,figsize=(15,7))
         
        for ax,t,p,c1,c2 in zip([ax1,ax2,ax3],[0,0,90],[0,90,90],[0,2,2],[1,1,0]):
            
            C = sph.Camera(r='infinity',t=t, p=p, roll=0, xsize=ext, ysize=ext,
                       x=c[0],y=c[1],z=c[2],extent=[-dl,dl,-dl,dl]) 
        
            S = sph.Scene(P,C)
            R = sph.Render(S)
            img = np.log10(R.get_image())
            extent = R.get_extent()
            ax.imshow(img,cmap=cmaps.twilight())
        
       
        ax1.text(0.1,0.9,'$\mathrm{log_{10}}(M_{\star} \,/\, \mathrm{M_{\odot}}) = %.2f$'%\
                 np.log10(mstar["%02d"%region][tag][_idx] * 1e10), 
                 transform=ax1.transAxes)


        for ax in [ax1,ax2,ax3]:
            ax.xaxis.set_major_formatter(FuncFormatter(lambda x, pos: (x/convers)*1e3))
            ax.yaxis.set_major_formatter(FuncFormatter(lambda x, pos: (x/convers)*1e3))
            ax.set_xlabel('$\mathrm{kpc}$',size=15)
            ax.set_ylabel('$\mathrm{kpc}$',size=15)            
            ax.add_patch(patches.Rectangle(((dl-0.006) * convers, (dl-0.006) * convers),
                         12/1e3 * convers, 12/1e3 * convers, linewidth=1,
                         edgecolor='white', facecolor='none'))
 
        
        fig.savefig('plots/gas_distribution_r%02d_i%02d.png'%(region,i), dpi=250)
        # fig.show()
        
