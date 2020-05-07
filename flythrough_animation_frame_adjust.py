#!/cosma/home/dp004/dc-rope1/.conda/envs/flares-env/bin/python
import matplotlib as ml
ml.use('Agg')
import numpy as np
from sphviewer.tools import cmaps, Blend
import matplotlib.pyplot as plt
from flythrough_animation import single_sphere
import sys
from guppy import hpy; h=hpy()


def get_normalised_image(img, vmin=None, vmax=None):

    if vmin == None:
        vmin = np.min(img)
    if vmax == None:
        vmax = np.max(img)

    img = np.clip(img, vmin, vmax)
    img = (img - vmin) / (vmax - vmin)

    return img


def single_frame(reg, snap, num):

    # Get images
    img_gas = np.load('animationdata/gas_animationdata_reg' + reg + '_snap' + snap + '_angle%05d.npy'%num)
    img_dm = np.load('animationdata/dm_animationdata_reg' + reg + '_snap' + snap + '_angle%05d.npy'%num)

    # Contrast stretching
    # p2, p98 = np.percentile(img_gas, (50, 99.9))
    # img_gas = exposure.rescale_intensity(img_gas, in_range=(p2, p98))
    # p2, p98 = np.percentile(img_dm, (50, 100))
    # img_dm = exposure.rescale_intensity(img_dm, in_range=(p2, p98))
    # print(p2, p98)
    # Set up colormaps
    cmap_gas = cmaps.twilight()
    # cmap_dm = ml.cm.Greys_r

    # Convert images to rgb arrays
    rgb_gas = cmap_gas(get_normalised_image(img_gas, vmin=8, vmax=12))
    # rgb_dm = cmap_dm(get_normalised_image(img_dm))

    # blend = Blend.Blend(rgb_dm, rgb_gas)
    # rgb_output = blend.Overlay()
    rgb_output = rgb_gas

    fig = plt.figure(figsize=(4, 4))
    ax = fig.add_subplot(111)

    ax.imshow(rgb_output, origin='lower')
    ax.tick_params(axis='both', left=False, top=False, right=False, bottom=False, labelleft=False,
                   labeltop=False, labelright=False, labelbottom=False)

    fig.savefig('plots/spheres/All/edit_all_parts_animation_reg' + reg + '_snap' + snap + '_angle%05d.png'%num,
                bbox_inches='tight')
    plt.close(fig)


# Define softening lengths
csoft = 0.001802390 / 0.677

reg, snap = '30', '010_z005p000'
print(int(sys.argv[1]))
try:
    single_frame(reg, snap, num=int(sys.argv[1]))
except FileNotFoundError:
    print("Need to generate this file:", reg, snap)
    single_sphere(reg, snap, soft=csoft, num=int(sys.argv[1]))
    single_frame(reg, snap, num=int(sys.argv[1]))