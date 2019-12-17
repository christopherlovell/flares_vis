import numpy as np
import matplotlib.pyplot as plt

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

