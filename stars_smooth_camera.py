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

# ## get input
# if len(sys.argv) > 1:
#     n1 = int(sys.argv[1])
#     n2 = int(sys.argv[2])
#     nrange = np.arange(n1,n2)
# else:
#     nrange = np.arange(0,360)

## particle properties

coods = E.readArray("SNAPSHOT", sim, tag, "/PartType4/Coordinates", numThreads=1)
pmass = E.readArray("SNAPSHOT", sim, tag, "/PartType4/Mass", numThreads=1)
phsml = E.readArray("SNAPSHOT", sim, tag, "/PartType4/SmoothingLength", numThreads=1)

## subhalo properties

sh_cop = E.readArray("SUBFIND", sim, tag, "/Subhalo/CentreOfPotential", numThreads=1)
sh_mstar = E.readArray("SUBFIND", sim, tag, "/Subhalo/Stars/Mass", numThreads=1)
spin = E.readArray("SUBFIND", sim, tag, "/Subhalo/GasSpin", numThreads=1)

## set centre of box

idx = np.argsort(sh_mstar)[::-1][0]
a,b,c = sh_cop[idx]      # use most massive (mstar) halo

## Align with spin axis of galaxy

s = spin[idx]
t = np.arctan(s[0]/s[2]) * 180./np.pi
p = np.arctan(s[1]/s[2]) * 180./np.pi

## Create particle and camera objects

P = sph.Particles(np.array(coods - [a,b,c]), pmass / pmass.min(), hsml = phsml)

# C = sph.Camera(x=0,y=0,z=0,
#                r=1,zoom=1,
#                t=t,p=p,roll=0,
#                xsize=4000,ysize=2250)  # 16:9




anchors = {}
anchors['sim_times'] = [0.0,'same','same','same','same','same','same']
anchors['id_frames'] =  [0,180,750,840,930,1500,1680]
anchors['r']         =  [1,'same','same','same','same','same','same']
anchors['id_targets']=  [0,'same','same','same','same','same','same']
anchors['t']         = [t,'same','same','same','same','same','same']
anchors['p']         = [p,'pass','pass','pass','pass','pass',p+900]
anchors['zoom']      = [1.,'same','same',9,'same','pass',1]
anchors['extent']    = [10, 'same','same','same','same','same',30]

from sphviewer.tools import camera_tools
targets = [[0,0,0]]
cam_data = camera_tools.get_camera_trajectory(targets,anchors)


for i,d in enumerate(cam_data):

    d['xsize'] = 4000
    d['ysize'] = 2250
    d['roll'] = 0

    print("p = %s | zoom = %s"%(d['p'],d['zoom']))
    sys.stdout.flush()

    S = sph.Scene(P)

    ## update scene camera
    S.update_camera(**d)

    R = sph.Render(S)
    
    ## Get image and plot
    R.set_logscale()
    img = R.get_image()
    # img = sph_cmaps.desert()(vis_util.get_normalized_image(img,vmin=0.4,vmax=3.2))
    img = plt.get_cmap('gray')(vis_util.get_normalized_image(img,vmin=None,vmax=1.2))

    fig, ax = vis_util.plot_img(img, R.get_extent())

    fig.savefig('movie_images/stars_smoothcam_testA_%03d.png'% i, bbox_inches='tight', pad_inches=0)

    plt.close()


