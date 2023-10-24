import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

from abc import ABC, abstractmethod
from typing import List

from src.text.config import text_stage_kwargs, text_nums_kwargs
from src.pictureconfig.config import pic_global

class ParseStrategy(ABC):
    @abstractmethod
    def prepare_string_list(self, arr_of_labels: np.ndarray) -> List[str]:
        pass

# :D można dodać argumenty do strategii np: 
# -> argument justowania 
# -> jaki symbol z prawej lub lambde przekształacającą liczbę
class Just(ParseStrategy):
    def prepare_string_list(self, arr_of_labels: np.ndarray) -> List[str]:
        justing = np.vectorize(lambda string : string.rjust(3))
        result:np.ndarray = justing(arr_of_labels)
        return result.tolist()

def label_stage(
    ax: plt.Axes,
    stage: int,
    label: str,
    labels_column: np.ndarray,
    parse_strategy: ParseStrategy,
    apply_colorQ: bool,
    cmap_list: list,
    cmap_arg: float,
    text_stage_kwargs:dict=text_stage_kwargs,
    text_nums_kwargs:dict=text_nums_kwargs
):
    """Function puts labels and numbers to the stage,
    cell example:
        import numpy as np
        import matplotlib as mpl
        import matplotlib.pyplot as plt
        from src.text.text import Just
        from src.text.text import label_stage
        fig, ax = plt.subplots()
        ax.set_facecolor('#393862')
        plt.xlim(0, 2)
        plt.ylim(0, 1.5)
        def foo(list):
            return mpl.colors.LinearSegmentedColormap.from_list(
                                'colormap', list, N=256, gamma=1.0)
        color_map_list = list(
            map(foo,[['w','r'], ['b','k'], ['r','b'], ['g','w']])
            )
        plt.xlim(0, 2)
        plt.ylim(0, 1.5)
        label_stage(
            ax=ax,
            stage=0,
            label='Matplotlib',
            parse_strategy=Just(),
            labels_column=np.array([34,27,11,12]).astype(str),
            apply_colorQ= True,
            cmap_list=color_map_list,
            cmap_arg=0.25)
        plt.show()
    """

    # patch for text
    x0, y0 = stage * pic_global["stage_width"], pic_global["funnel_height"]
    x1, y1 = (stage + 1) * pic_global["stage_width"], pic_global["picture_height"]
    width, height = x1 - x0, y1 - y0
    box = Rectangle((x0, y0), width, height, fc="none", ec="w")
    ax.add_patch(box)

    # drawing top label, first place with <text> valiable
    label_gaps = {"box_gap": 0.02, "first_no_XY": (0, 0)}
    gap = label_gaps["box_gap"]
    text = ax.text(x0 + gap, y1 - gap, label, **text_stage_kwargs)

    # the column of labels
    strings_to_annotate = parse_strategy.prepare_string_list(labels_column)
    
    # temporary storage of color default to numbers
    default_num_color = text_nums_kwargs["color"]

    # annotate felative to previous <text> valiable
    for i, num_str in enumerate(strings_to_annotate):
        if apply_colorQ == True:
            text_nums_kwargs['color'] = cmap_list[i](cmap_arg)
        text = ax.annotate(
            num_str,
            xycoords=text,
            xy=(0,0),#label_gaps['first_no_XY'] if i == 0 else (1, 0),
            va='top',
            ha='left' if i == 0 else 'left',
            **text_nums_kwargs
        )
    text_nums_kwargs["color"] = default_num_color

    return text

# # text preview
# import matplotlib.pyplot as plt
# from matplotlib.patches import Rectangle
# fig, ax = plt.subplots()
# ax.set_facecolor('#393862')
# plt.xlim(0, 2)
# plt.ylim(0, 1.5)
# ax.set_aspect('equal')
# title_dict = dict(
#     size=20,
#     color="tab:orange",
#     va='top', ha='left',
#     family='sans-serif',
#    weight="bold", 
#     )
# numbs_dict = dict(
#     size=20,
#     color='#e3dac9', 
#     weight='bold', 
#     family='sans-serif'
#     )
# x0, y0, x1, y1 = 0.0, 1, 1, 1.5
# width, height = x1 - x0, y1 - y0
# rect = Rectangle((x0, y0), width, height, fc="none", ec='y')#, ec="none")
# ax.add_patch(rect)
# gap = 0.02
# text = ax.text(x0+gap, y1-gap, "Matplotlib", **title_dict)
# text = ax.annotate(
#     "34 %", xycoords=text, xy=(0.05, -0.25), va="top", ha='left', **numbs_dict)
# text = ax.annotate(
#     "27 %", xycoords=text, xy=(1, 0), va="top", ha='right', **numbs_dict)
# text = ax.annotate(
#     "11 %", xycoords=text, xy=(1, 0), va="top",ha='right', **numbs_dict)
# plt.show()

# # look no further:
# import matplotlib.pyplot as plt
# from matplotlib.transforms import Affine2D
# from matplotlib.textpath import TextPath
# from matplotlib.font_manager import FontProperties
# from matplotlib.patches import PathPatch

# fig, ax = plt.subplots(3, dpi=100)
# ax[0].set(xlim=(-0.2, 3.2), ylim=(-0.2, 1.2))
# ax[1].set(xlim=(0.3, 0.6), ylim=(0.95, 1.05))
# ax[2].set(xlim=(2.3, 2.9), ylim=(0.95, 1.05))

# from matplotlib.font_manager import FontProperties

# fp = FontProperties(family='serif')
# for i in [0,1,2]:
#     path = TextPath((0, 0), "ABC", size=1, prop=fp)
#     p = PathPatch(path, facecolor='orange', lw=1)
#     transform = Affine2D().scale(100/73)
#     p.set_transform(transform+ax[i].transData)
#     ax[i].add_patch(p)
#     ax[i].set_aspect('equal')

#     ax[i].hlines(y=[0,1], xmin=-1, xmax=4)

# plt.show()

