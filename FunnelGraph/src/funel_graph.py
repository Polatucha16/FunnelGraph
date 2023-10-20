from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
# from matplotlib.path import Path
from matplotlib.patches import PathPatch

from src.interpolating_function import inter_poly
from src.gradient import gradient_image, cmaps_dict

class FunelGraph():
    def __init__(self, data_dict=None, path='data', pts=100):
        if data_dict is None:
            self.data_dict = {
                'labels': None,
                'colors': None,
                'values': None
                }
        self.pts = pts
        self.names_mpl_cmaps = [item for row in cmaps_dict.values() for item in row]
            
    def load_data(self, file_name:str='data.csv'):
        self.root = Path(__file__).parents[1]
        data_path = self.root / 'data'

        # load pandas dataframe
        self.df:pd.DataFrame = pd.read_csv(
            filepath_or_buffer=data_path/file_name, 
            delimiter=';')
        
        # labels
        if self.data_dict['labels'] is None:
            self.data_dict['labels'] = self.df.columns.to_list()
        
        # numeric data
        self.data_dict['values'] = self.df.to_numpy()
        pass
    
    def data_for_labels(self):

        self.label_text_kwargs = dict(fontsize=15, color='C1')
        self.number_text_kwargs = dict(fontsize=15, color='w')

        arr:np.ndarray = self.data_dict['values']
        self.sums_of_stages = np.sum(a=arr, axis=0)
 
    def data_normalisation(self):
        """ Creates guide for patches from self.data_dict['values'].
            Variable self.points_to_plot stores Y values for the picture 
            of size M by 1 through which consecutive patches will go.
            The goal on this normalisation is to center the vertical intervals
            in the center of the picture i.e. centers of vertical
            intervals will be (k, 0.5) for k in integers from 0 to M.
            Arguments:
                self.data_dict['values'] volumes of categories in stages t0 draw.
                    Each row is single category, each column is stage,
                    there are M columns and N categories.
            Result:
                Result is written into self.points_to_plot.
                Resulting array has shape (N+1, M).
                First row of the resulting array are Y coordinates guiding 
                the lowest line and successive rows guide lines following 
                from the bottom up.
            """
        arr:np.ndarray = self.data_dict['values']
        max_of_col_sums = np.max(np.sum(a=arr, axis=0))
        cumsum = np.cumsum(np.flip(arr/max_of_col_sums,axis=0), axis=0)
        # last row of cumsum has heights of stages
        starting_level = 0.5-(cumsum[-1]/2) 
        increments = np.tile(starting_level, reps=(cumsum.shape[0], 1)) + cumsum
        self.points_to_plot = np.vstack((starting_level, increments))
    
    def create_paths(self):
        """ Paths are created in the following way:
            For an array of guiding points written in self.points_to_plot =
                [[y00, y01, ..., y0m]
                 [y10, y11, ..., y1m]
                 :
                 [yn0, y11, ..., ynm]],
            we produce first path: 
             from first two rows by interpolating values:
                from y00 to y01, then from y01 to  y02, ..., then from y0(m-1) to y0m
             then concatenate the above with REVERSED interpolating values of:
                from y10 to y11, then from y11 to  y12, ..., then from y1(m-1) to y1m
             make X coordinates by two copies of np.arrange(0, M, pts*m) one going forward
             the other REVERSED.
            Then make similar paths for the rest of pairs of rows (y1, y2), (y2, y3), ..., (y(n-1), yn).
        """
        lines, stages = self.points_to_plot.shape

        # Create X coordinate array. Note: there are one less starting points than 'stages'.
        x = np.linspace(start=0, stop=1, num=self.pts) # for each stage
        xx = np.hstack(tup=[ i + x for i in range(stages-1) ]) # for final path

        self.paths = []
        for (base, top) in zip(self.points_to_plot[:-1], self.points_to_plot[1:]):

            base_zip = zip(base[:-1], base[1:])
            base_list_of_waves = [inter_poly(x, parmaters=[0, v0, 1, v1]) for (v0, v1) in base_zip ]
            base_wave = np.hstack(tup=base_list_of_waves)

            top_zip = zip(top[:-1], top[1:])
            top_list_of_waves = [inter_poly(x, parmaters=[0, v0, 1, v1]) for (v0, v1) in top_zip ]
            top_wave = np.hstack(tup=top_list_of_waves)

            current_Y_path = np.hstack(tup=(base_wave, np.flip(top_wave)))
            current_X_path = np.hstack(tup=(xx,np.flip(xx)))
            xy = np.vstack(tup=(current_X_path, current_Y_path))
            self.paths.append(xy)

    def prepare(self, **kwargs):
        self.load_data()
        self.data_normalisation()
        self.create_paths()

    def set_colors(self, colors=['autumn', 'copper', 'viridis', 'Oranges']):
        """ Argument colors is a list with elements of the form:
                - single string with color in hex or colorname eg:
                    '#393862', 'blue', or 'y'.
                - single matplotlib colormap name eg:
                    'viridis', 'spring'.
                - list of colors eg:
                    ['#393862','blue']
                List of colors are passed to mpl.colors.LinearSegmentedColormap
                to create colormap.
            """
        self.cmaps_for_patches = []
        if self.data_dict['colors'] is not None:
            colors = self.data_dict['colors']
            
        for i ,color in enumerate(colors):
            if color in self.names_mpl_cmaps or (
                color[:-2] in self.names_mpl_cmaps and color[-2:] == '_r'):
                self.cmaps_for_patches.append(color)
            elif isinstance(color, list):
                self.cmaps_for_patches.append(
                    mpl.colors.LinearSegmentedColormap.from_list(
                        'color_patch'+str(i), color, N=256, gamma=1.0)
                )
            else:
                self.cmaps_for_patches.append(
                    mpl.colors.LinearSegmentedColormap.from_list(
                        'color_patch'+str(i), [color, color], N=256, gamma=1.0)
                )
        self.cmaps_len = len(self.cmaps_for_patches)

    def draw(self, background_color:str='#393862', **kwargs):
        # my kind of blue #27557b
        # nice purpleish #393862
        self.set_colors(**kwargs)

        lines, stages = self.points_to_plot.shape

        fig, ax = plt.subplots()
        ax.set(xlim=(0, stages-1), ylim=(-0.05, 1.50))

        # vertival guides
        ax.vlines(np.arange(stages), -2, 2, colors='w', lw=0.5)
        
        # the texts
        for stage in range(stages-1):
            # ax.text(stage+0.5, 1.4, self.data_dict['labels'][stage], **self.label_text_kwargs)
            
            left = stage + 0.05
            top_for_name = 1.5 - 0.05
            ax.text(left, top_for_name, 
                    self.data_dict['labels'][stage],
                    horizontalalignment='left',
                    verticalalignment='top',
                    **self.label_text_kwargs)
            
            top_for_numbers = 1.4 - 0.1
            ax.text(left, top_for_numbers, 
                    str(self.sums_of_stages[stage]),
                    horizontalalignment='left',
                    verticalalignment='top',
                    **self.number_text_kwargs)

        ax.set_facecolor(background_color)
        # ax.get_xaxis().set_visible(False)
        # ax.get_yaxis().set_visible(False)

        for path_no, path in enumerate(self.paths):
            
            # numpy arr -> matplotlib Patches on ax Axes
            current_path = mpl.path.Path(path.T)
            patch = PathPatch(current_path, facecolor='none', edgecolor='k', linewidth=0.1)
            ax.add_patch(patch)

                #drawing a gradient
            im = gradient_image(
                    ax, 
                    direction=1, 
                    cmap_range=(0.1, 0.9),
                    extent=(0, 1, 0, 1), 
                    transform=ax.transAxes,
                    # cmap=mpl.colormaps[color],
                    cmap=self.cmaps_for_patches[path_no % self.cmaps_len],
                    alpha=1,
                    clip_path=patch, 
                    clip_on=True
                    )
        return im
            
