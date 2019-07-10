import eagle as E
import numpy as np
import pandas as pd

import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
import sphviewer as sph
from sphviewer.tools import QuickView, cmaps

direc = '/cosma7/data/dp004/dc-love2/data/G-EAGLE/geagle_0000/data'
tag = '009_z006p188'
pdark = E.readArray("SNAPSHOT", direc, tag, "/PartType1/Coordinates", numThreads=1, noH=True, physicalUnits=False)
mass_a100 = np.sum(E.readArray("SUBFIND", direc, tag, "Subhalo/ApertureMeasurements/Mass/100kpc", numThreads=1, noH=True),axis=1) * 1e10
coods = E.readArray("SUBFIND", direc, tag, "Subhalo/CentreOfMass", numThreads=1, noH=True, physicalUnits=False)

# choose a galaxy
idx = np.argmax(mass_a100)
c = coods[idx]

## quicker filter..
dl = 5
pmask = (pdark[:,0] > c[0]-dl)
pmask[pmask] = (pdark[pmask,0] < c[0]+dl)
pmask[pmask] = (pdark[pmask,1] > c[1]-dl)
pmask[pmask] = (pdark[pmask,1] < c[1]+dl)
pmask[pmask] = (pdark[pmask,2] > c[2]-dl)
pmask[pmask] = (pdark[pmask,2] < c[2]+dl)

# pmask = ((pdark[:,0] > coods[0]-dl) & (pdark[:,0] < coods[0]+dl) &\
#          (pdark[:,1] > coods[1]-dl) & (pdark[:,1] < coods[1]+dl) &\
#          (pdark[:,2] > coods[2]-dl) & (pdark[:,2] < coods[2]+dl))

print(len(pdark),np.sum(pmask))

# qv = QuickView(pdark[pmask],r='infinity',plot=False)
# qv.imshow()

ext=500 # number of pixels in image
convers = ext/(2*dl) # conversion factor

P = sph.Particles(pdark[pmask],mass=np.ones(np.sum(pmask)))

fig,(ax1,ax2,ax3) = plt.subplots(1,3,figsize=(15,7))

for ax,t,p,c1,c2 in zip([ax1,ax2,ax3],[0,0,90],[0,90,90],[0,2,2],[1,1,0]):
    
    C = sph.Camera(r='infinity',t=t, p=p, roll=0, xsize=ext, ysize=ext,
               x=c[0],y=c[1],z=c[2],extent=[-dl,dl,-dl,dl]) 

    S = sph.Scene(P,C)
    R = sph.Render(S)
    img = np.log10(R.get_image())
    extent = R.get_extent()
    
    ax.imshow(img,cmap=cmaps.twilight())


for ax in [ax1,ax2,ax3]:
    ax.xaxis.set_major_formatter(FuncFormatter(lambda x, pos: x/convers))
    ax.yaxis.set_major_formatter(FuncFormatter(lambda x, pos: x/convers))
    ax.set_xlabel('$\mathrm{Mpc}$',size=15)
    ax.set_ylabel('$\mathrm{Mpc}$',size=15)


fig.savefig('plots/pysph_demo.png', dpi=250)
fig.show()

