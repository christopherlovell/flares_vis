import sys
import os
import numpy as np

import matplotlib as ml
ml.use('Agg')
import matplotlib.pyplot as plt

import sphviewer as sph
from sphviewer.tools import cmaps, Blend, camera_tools

from flaresvis import spherical_region, get_normalized_image, get_particle_data, cutout_particles


def getimage(snap, num, data, part_type, overwrite=False, P=None, S=None):
    
    if overwrite:
        i = data[num]
        i['xsize'] = 5000
        i['ysize'] = 5000
        i['roll'] = 0
        S.update_camera(**i)
        R = sph.Render(S)
        R.set_logscale()
        img = R.get_image()
        extent = R.get_extent()

        np.save('animationdata/ptype%s_animationdata_reg%s_snap%s_angle%05d.npy'%(part_type,reg,snap,num), img)
    else:
        img = np.load('animationdata/ptype%s_animationdata_reg%s_snap%s_angle%05d.npy'%(part_type,reg,snap,num))
        extent = [-45,45,45,-45]


    return img, extent


def apply_cmap(img,cmap,vlims):
    print("Setting fixed vmin and vmax")
    # vmin = 3.5
    # vmax = 7

    vmin,vmax = vlims
    
    # vmax = img.max()
    # vmin = vmax * 0.5
    print("vmin:",vmin,"| vmax:",vmax)

    rgb = cmap(get_normalized_image(img, vmin=vmin, vmax=vmax))

    return rgb


def single_sphere(reg, snap, soft, num, part_type, cmap, vlims, runall=True):

    if runall:
        # Define path
        path = '/cosma/home/dp004/dc-rope1/FLARES/FLARES-1/G-EAGLE_' + reg + '/data'
    
        poss, masses, smls = get_particle_data(path, snap, part_type=part_type, soft=soft)

        # Get the spheres centre
        centre, radius, mindist = spherical_region(path, snap)

        # Cutout particles
        poss, masses, smls = cutout_particles(poss, masses, smls, centre, radius)
    
        print('There are %i particles (type %s) in the region'%(len(masses),part_type))
        
        # Set up particle objects
        P = sph.Particles(poss, mass=masses, hsml=smls)

        # Initialise the scene
        S = sph.Scene(P)


    targets = [[0,0,0]]#,0,0,0,0,0,0]
    
    # Define the box size
    lbox = (15 / 0.677) * 2

    # Define anchors dict for camera parameters
    anchors = {}
    anchors['sim_times'] = [0.0, 'same', 'same', 'same', 'same', 'same', 'same', 'same', 'same']
    anchors['id_frames'] = [0, 90, 180, 270, 360, 450, 540, 630, 720]
    anchors['id_targets'] = [0, 'same', 'same', 'same', 'same', 'same', 'same', 'same', 'same']
    anchors['r'] = [lbox * 3 / 4, 'same', 'same', 'same', 'same', 'same', 'same', 'same', 'same']
    anchors['t'] = [0, 'same', 'same', 'same', 'same', 'same', 'same', 'same', 'same']
    anchors['p'] = [0, 'pass', 'pass', 'pass', 'pass', 'pass', 'pass', 'pass', 360]
    anchors['zoom'] = [1., 'same', 'same', 'same', 'same', 'same', 'same', 'same', 'same']
    anchors['extent'] = [10, 'same', 'same', 'same', 'same', 'same', 'same', 'same', 'same']
    
    # Define the camera trajectory
    data = camera_tools.get_camera_trajectory(targets, anchors)

    for N in np.arange(num*N_block,(num*N_block)+N_block):
        print("N:",N,'| p:',data[N]['p'])

        # Get images
        if runall:
            img, extent = getimage(snap, N, data, part_type=part_type, overwrite=True, P=P, S=S)
        else:
            img, extent = getimage(snap, N, data, part_type=part_type, overwrite=False)


        rgb = apply_cmap(img,cmap,vlims)

        fig = plt.figure(figsize=(16,9), frameon=False)

        ax = fig.add_subplot(111)
    
        # set extent to 16:9 ratio
        ax.set_xlim(extent[0] * 16/9, extent[1] * 16/9)
        
        ax.imshow(rgb, origin='lower', aspect='equal', extent=extent)
        ax.tick_params(axis='both', left=False, top=False, right=False, 
                       bottom=False, labelleft=False, labeltop=False, 
                       labelright=False, labelbottom=False)

        ax.set_facecolor(cmap(0.0)) # (0.95588623, 0.91961077, 0.95812116))
        fname = 'plots/spheres/All/all_parts_animation_reg%s_snap%s_ptype%s_angle%05d.png'%(reg,snap,part_type,N)
        print("Saving:",fname)
        fig.savefig(fname, dpi=300, bbox_inches='tight')
        plt.close(fig)


# Define softening lengths
csoft = 0.001802390 / 0.677

N_block = 20
reg, snap = 0, '010_z005p000'

if len(sys.argv) > 2:
    part_type = int(sys.argv[2])
else:
    part_type = 1

_cmaps = [cmaps.desert(),cmaps.twilight(),None,None,cmaps.mars()]
_cmap = _cmaps[part_type]

_vlims = [[10,14],[3.5,7],None,None,[8,14.4]]
_vlim = _vlims[part_type]

single_sphere("%02d"%reg, snap, soft=csoft, num=int(sys.argv[1]), part_type=part_type, cmap=_cmap, vlims=_vlim, runall=True)
