import numpy as np

import matplotlib as mpl
import matplotlib.pyplot as plt

# gradient drawing function from matplotlib examples:
# https://matplotlib.org/stable/gallery/lines_bars_and_markers/gradient_bar.html
def gradient_image(ax: plt.Axes, direction=0.5, cmap_range=(0, 1), **kwargs):
    """ cmap_range=(0, 1)
    Draw a gradient image based on a colormap.

    Parameters
    ----------
    ax : Axes
        The axes to draw on.
    direction : float
        The direction of the gradient. This is a number in
        range 0 (=vertical) to 1 (=horizontal).
    cmap_range : float, float
        The fraction (cmin, cmax) of the colormap that should be
        used for the gradient, where the complete colormap is (0, 1).
    **kwargs
        Other parameters are passed on to `.Axes.imshow()`.
        In particular, *cmap*, *extent*, and *transform* may be useful.
    """
    phi = direction * np.pi / 2
    v = np.array([np.cos(phi), np.sin(phi)])
    X = np.array([[v @ [1, 0], v @ [1, 1]], [v @ [0, 0], v @ [0, 1]]])
    a, b = cmap_range
    X = a + (b - a) / X.max() * X
    im = ax.imshow(X, interpolation="bicubic", aspect="auto", **kwargs)#, vmin=0, vmax=1, **kwargs)
    return im

# # pure color linear gradient preview
# import matplotlib as mpl
# mpl.colors.LinearSegmentedColormap.from_list(
#                     'tab:BluOra', ['tab:blue','tab:orange'], N=256, gamma=1.0
#                     )

# # cmaps_range vs. vmin, vmax of imshow
# import matplotlib.pyplot as plt
# from src.gradient.gradient import gradient_image
# fig, ax = plt.subplots()
# ax.set(xlim=(0, 1), ylim=(0, 1))
# ax = gradient_image(ax, direction=1, cmap='Reds', cmap_range=(-5,5), vmin=-1, vmax=1)
# plt.show()

# # checkered pattern interpolation preview,
# # https://matplotlib.org/stable/gallery/images_contours_and_fields/interpolation_methods.html
# import numpy as np
# import matplotlib.pyplot as plt
# fig, axs = plt.subplots(nrows=2, ncols=3, figsize=(6, 4))
# X = np.array([[0, 1, 0, 1],
#               [1, 0, 1, 0],
#               [0, 1, 0, 1],
#               [1, 0, 1, 0]])
# inter_name = [None, 'bilinear', 'bicubic', 'quadric', 'spline16', 'sinc']
# for ax, interpolation in zip(axs.flat,inter_name):
#     ax.imshow(X, interpolation=interpolation, cmap='viridis', clim=(0, 1), aspect='equal')
#     ax.set_title(str(interpolation))
#     ax.set_axis_off()
# plt.show()

# # multiply array by direction
# import numpy as np
# import matplotlib.pyplot as plt
# direction = 0.5
# phi = direction * np.pi / 2
# v = np.array([np.cos(phi), np.sin(phi)])
# res = 4
# # 0,1 checkerboard
# zero_one, one_zero = np.array([0,1]), np.array([1,0])
# even_row = np.tile(zero_one, reps=(1,res))
# odd__row = np.tile(one_zero, reps=(1,res))
# arr = np.zeros((2*res, 2*res))
# for row_no in range(2*res):
#     arr[row_no] = even_row if row_no % 2 == 0 else odd__row
# # array of points creation 
# x, y = np.linspace(0,1,2*res), np.linspace(0,1,2*res)
# m = np.transpose(a=np.array(np.meshgrid(x,y)), axes=(2,1,0))
# directed = (m.reshape(-1,2) @ v).reshape(2*res,2*res) 
# im_arg = np.multiply(arr, directed)
# fig, ax = plt.subplots()
# ax.imshow(im_arg, cmap='viridis', clim=(0, 1), aspect="auto", interpolation="spline16")
# plt.show()