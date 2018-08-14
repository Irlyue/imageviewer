import os
import numpy as np


def create_if_not_exists(path):
    if not os.path.exists(path):
        os.makedirs(path)


def load_colormap(n=255, normalized=True):
    """
    A colormap for displaying mask. Use it like this `plt.imshow(cmap[mask])` and you're
    good to go. Most of the time the default parameters would be ok.

    :param n: int, number of colors in the colormap
    :param normalized: boolean, whether to divide by 255.0 for normalization
    :return:
    """
    def bitget(byteval, idx):
        return (byteval & (1 << idx)) != 0

    dtype = 'float32' if normalized else 'uint8'
    cmap = np.zeros((n, 3), dtype=dtype)
    for i in range(n):
        r = g = b = 0
        c = i
        for j in range(8):
            r = r | (bitget(c, 0) << 7-j)
            g = g | (bitget(c, 1) << 7-j)
            b = b | (bitget(c, 2) << 7-j)
            c = c >> 3

        cmap[i] = np.array([r, g, b])

    cmap = cmap/255 if normalized else cmap
    return cmap