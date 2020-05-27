import numpy as np
import matplotlib.pyplot as plt

from scipy.optimize import curve_fit
from scipy.spatial import ConvexHull

import eagle_IO.eagle_IO as E


def plot_img(img, extent, figsize=(12,12)):
    """
    Plot img grid
    """
    fig = plt.figure(frameon=False)
    fig.set_size_inches(16,9)

    ax = plt.Axes(fig, [0.,0.,1.,1.])
    ax.set_axis_off()
    fig.add_axes(ax)


    ax.imshow(img, aspect='auto') # extent=extent, origin='lower')

    ax.get_xaxis().set_visible(False)
    ax.get_yaxis().set_visible(False)

    return fig, ax


def get_normalized_image(image, vmin=None, vmax=None):
    if(vmin == None):
        vmin = np.min(image)
    if(vmax == None):
        vmax = np.max(image)

    image = np.clip(image, vmin, vmax)
    image = (image-vmin)/(vmax-vmin)

    return image


def _sphere(coords, a, b, c, r):

    # Equation of a sphere
    x, y, z = coords[:, 0], coords[:, 1], coords[:, 2]

    return (x - a) ** 2 + (y - b) ** 2 + (z - c) ** 2 - r ** 2


def spherical_region(sim, snap, coods=None):
    """
    Inspired from David Turner's suggestion
    """

    if coods is None:
        print("Using dark matter particles to define region, Loading...")
        coods = E.read_array('PARTDATA', sim, snap, '/PartType1/Coordinates',
                           noH=True, physicalUnits=False, numThreads=4)  # dm particle coordinates

    hull = ConvexHull(coods)

    print('Defined convex hull')

    cen = [np.median(coods[:, 0]), np.median(coods[:, 1]), np.median(coods[:,2])]
    pedge = coods[hull.vertices]  #edge particles
    y_obs = np.zeros(len(pedge))
    p0 = np.append(cen, 15 / 0.677)

    print('Defined convex hull')

    popt, pcov = curve_fit(_sphere, pedge, y_obs, p0, method='lm', sigma=np.ones(len(pedge)) * 0.001)
    dist = np.sqrt(np.sum((pedge-popt[:3])**2, axis=1))
    centre, radius, mindist = popt[:3], popt[3], np.min(dist)

    print('computed fit')

    return centre, radius, mindist


def get_particle_data(path, snap, part_type, soft):

    # Get positions masses and smoothing lengths
    poss = E.read_array('SNAP', path, snap, 'PartType' + str(part_type) + '/Coordinates',
                        noH=True, physicalUnits=False, numThreads=8)
    if part_type != 1:
        masses = E.read_array('SNAP', path, snap, 'PartType' + str(part_type) + '/Mass',
                              noH=True, physicalUnits=False, numThreads=8) * 10 ** 10
        smls = E.read_array('SNAP', path, snap, 'PartType' + str(part_type) + '/SmoothingLength',
                            noH=True, physicalUnits=False, numThreads=8)
    else:
        masses = np.ones(poss.shape[0])
        smls = np.full_like(masses, soft)

    return poss, masses, smls


def cutout_particles(poss, masses, smls, centre, r):
    """
    Cut out all the particles
    """

    # Centre particles
    poss -= centre

    # Remove boundary particles
    r = np.linalg.norm(poss, axis=1)
    okinds = r < 14 / 0.677
    poss = poss[okinds, :]
    masses = masses[okinds]
    smls = smls[okinds]

    return poss, masses, smls


