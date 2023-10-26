import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.path import Path
from matplotlib.patches import PathPatch

from src.funnelshape.interpolating_function import inter_poly
from src.text.text import draw_lists_of_strings  # label_stage, Just
from src.gradient.gradient import gradient_image
from src.dataloader.dataloader import pd_dataloader
from src.picture_config.config import picture_size


# to implement: pic_global["stage_width"], pic_global["funnel_height"]
class FunelGraph:
    def __init__(self, data_dict=None, path="data", pts=100):
        if data_dict is None:
            self.data_dict = {
                "graph_data": None,
                "data_labels": None,
                "label_data": None,
                "labels": None,
                "colors": None,
            }
        self.pts = pts
        self.names_mpl_cmaps = plt.colormaps()

    def load_data(self, df: pd.DataFrame):
        self.data_dict["graph_data"] = df.to_numpy()
        self.data_dict["data_labels"] = df.columns.to_list()

    def load_labels(self, df: pd.DataFrame):
        self.data_dict["label_data"] = df.to_numpy().astype(str)
        self.data_dict["labels"] = df.columns.to_list()

    def normalize_data(self, normaliseQ: bool = True):
        """Fills object variables :
            self.points_to_plot,

        Creates guide for patches from self.data_dict['graph_data'].
        The goal of this normalisation is to rescale data volumes to fit (M,1) picture.
        Arguments:
            normaliseQ : True or False condition do we perform normalisation.
            self.data_dict['graph_data'] : np.ndarray of shape (N, M) representing
                volumes of N categories in all of M stages.
        Result:
            self.points_to_plot : np.ndarray of shape (N+1, M+1)
                Rows of the resulting array are Y coordinates guiding path
                of consecutive points (i, *) for i in 0, 1, 2, ..., M+2.
                First row is the lowest path and successive rows guide lines following
                from the bottom up.
        """

        def add_copy_of_last_column(arr):
            """We need to extend self.data_dict['graph_data'] of shape:(N, M)
            by a copy of the last column to execute the following labeling strategy:
                0 -> 1      is labeled with data from column 0
                1 -> 2      is labeled with data from column 1
                ...
                m-2 -> m-1  is labeled with data from column m-2
                m-1 -> m-1  is labeled with data from column m-1
            """
            return np.c_[arr, arr[:, -1]]

        if normaliseQ is True:
            arr: np.ndarray = add_copy_of_last_column(self.data_dict["graph_data"])
            max_of_col_sums = np.max(np.sum(a=arr, axis=0))
            cumsum = np.cumsum(np.flip(arr / max_of_col_sums, axis=0), axis=0)
            # last row of cumsum has heights of stages
            starting_levels = 0.5 - (cumsum[-1] / 2)
            increments = np.tile(starting_levels, reps=(cumsum.shape[0], 1)) + cumsum
            self.points_to_plot = np.vstack((starting_levels, increments))
        else:
            self.points_to_plot = self.data_dict["graph_data"]

    def create_paths(self):
        """Paths are created in the following way:
        For an array of guiding points written in self.points_to_plot =
            [[y00, y01, ..., y0m]
             [y10, y11, ..., y1m]
             :
             [yn0, y11, ..., ynm]],
        we produce first path:
         from first two rows by interpolating graph_data:
            from y00 to y01, then from y01 to  y02, ..., then from y0(m-1) to y0m
         then concatenate the above with REVERSED interpolating graph_data of:
            from y10 to y11, then from y11 to  y12, ..., then from y1(m-1) to y1m
         make X coordinates by two copies of np.arrange(0, M, pts*m) one going forward
         the other REVERSED.
        Then make similar paths for the rest of pairs of rows (y1, y2), (y2, y3), ..., (y(n-1), yn).
        """
        self.lines, self.stages = self.points_to_plot.shape
        width = picture_size['stage_width']

        # Create X coordinate array. Note: there are one less starting points than 'stages'.
        x = np.linspace(start=0, stop=width, num=self.pts)  # for each stage
        xx = np.hstack(tup=[i*width + x for i in range(self.stages - 1)])  # for final path

        self.paths = []
        for base, top in zip(self.points_to_plot[:-1], self.points_to_plot[1:]):
            base_zip = zip(base[:-1], base[1:])
            base_list_of_waves = [
                inter_poly(x, parmaters=[0, v0, width, v1]) for (v0, v1) in base_zip
            ]
            base_wave = np.hstack(tup=base_list_of_waves)

            top_zip = zip(top[:-1], top[1:])
            top_list_of_waves = [
                inter_poly(x, parmaters=[0, v0, width, v1]) for (v0, v1) in top_zip
            ]
            top_wave = np.hstack(tup=top_list_of_waves)

            current_Y_path = np.hstack(tup=(base_wave, np.flip(top_wave)))
            current_X_path = np.hstack(tup=(xx, np.flip(xx)))
            xy = np.vstack(tup=(current_X_path, current_Y_path))
            self.paths.append(xy)
        self.paths.reverse()

    def prepare(
        self, data_path="data/data.csv", label_path="data/labels.csv", **kwargs
    ):
        self.load_data(pd_dataloader(path=data_path))
        self.load_labels(pd_dataloader(path=label_path))
        self.normalize_data(**kwargs)
        self.create_paths()

    def set_colors(
        self,
        colors=[
            ["#009245", "#FCEE21"],
            ["#1BFFFF", "#7678d4"],
            ["#FCEE21", "#009245"],
            ["#FBB03B", "#D4145A"],
            ["#C33764", "#1BFFFF"],
        ],
        **kwargs
    ):
        """Argument colors should be a list of elements, each element can be in the one
        of the following three possible formats:
            - single string with color in hex or colorname eg:
                '#393862', 'blue', or 'y'.
            - single matplotlib colormap name eg:
                'viridis', 'spring'.
            - list of colors eg:
                ['#393862','blue']
            List of colors are passed to mpl.colors.LinearSegmentedColormap
            to create colormap.
        """
        cmaps = []

        for i, color in enumerate(colors):
            if color in self.names_mpl_cmaps:
                # matplotlib named colormaps
                cmaps.append(color)
            elif isinstance(color, list):
                # list of named colors
                cmaps.append(
                    mpl.colors.LinearSegmentedColormap.from_list(
                        "color_patch" + str(i), color, N=256, gamma=1.0
                    )
                )
            else:  # single color
                cmaps.append(
                    mpl.colors.LinearSegmentedColormap.from_list(
                        "color_patch" + str(i), [color, color], N=256, gamma=1.0
                    )
                )
        self.data_dict["colors"] = cmaps
        self.cmaps_len = len(cmaps)

    def draw_graph(self):
        num_of_colors = len(self.data_dict["colors"])
        for path_number, np_path in enumerate(self.paths):
            np_path: np.ndarray

            # path:np.ndarray -> patch: mpl.patches.PathPatch to clip gradients from imshow
            mpl_path = Path(np_path.T)
            mpl_patch = PathPatch(
                mpl_path, facecolor="none", edgecolor="k", linewidth=0.1
            )
            self.ax.add_patch(mpl_patch)

            # drawing a gradient that will be visibile only on mpl_patch
            gradient_image(
                ax=self.ax,
                direction=1,
                cmap_range=(0, 1),
                extent=(0, 1, 0, 1),
                transform=self.ax.transAxes,
                cmap=self.data_dict["colors"][path_number % num_of_colors],
                alpha=1,
                clip_path=mpl_patch,
                clip_on=True,
            )

    def draw_labels(self, **kwargs):
        for stage, title in enumerate(self.data_dict["labels"]):
            s_args = []
            first__list_of_strings = [title]
            second_list_of_strings = list(self.data_dict["label_data"][:, stage])
            s_args.append(first__list_of_strings)
            s_args.append(second_list_of_strings)
            # print(s_args) # noob debugging
            draw_lists_of_strings(
                ax=self.ax,
                xy=(stage*picture_size["stage_width"], picture_size["funnel_height"]),
                width=picture_size["stage_width"],
                height=picture_size["picture_height"] - picture_size["funnel_height"],
                s_args=s_args,
                **kwargs
            )

    def draw_vertical_lines(self):
        self.ax.vlines(np.arange(self.stages)*picture_size['stage_width'], -2, 2, colors="w", lw=0.5)

    def adjust_picture(
        self,
        background_color: str = "#393862",
        aspect: float = 1,
        axesQ: bool = True,
        **kwargs
    ):
        self.ax.set_facecolor(background_color)
        self.fig.set_facecolor(background_color)
        self.ax.set_frame_on(False)
        self.ax.set(xlim=(0, (self.stages - 1)*picture_size['stage_width']), 
                    ylim=(-0.01, picture_size['picture_height']))
        # self.ax.axis('off')
        self.ax.set_aspect(aspect)
        self.ax.get_xaxis().set_visible(axesQ)
        self.ax.get_yaxis().set_visible(axesQ)

    def draw(self, **kwargs):
        self.set_colors(**kwargs)
        self.fig, self.ax = plt.subplots(
            figsize=(
                (self.stages - 1)*picture_size['stage_width']*picture_size['size'],
                 picture_size['picture_height']*picture_size['size']))
        self.adjust_picture(**kwargs)
        self.draw_graph()
        self.draw_labels(**kwargs)
        self.draw_vertical_lines()
        return self.ax
