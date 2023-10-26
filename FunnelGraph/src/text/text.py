import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from matplotlib.axes import Axes
from matplotlib.text import Annotation
from matplotlib.transforms import Bbox

from abc import ABC, abstractmethod
from typing import List, Tuple

from src.text.config import title_kwargs, label_kwargs
from src.text.text_anchors import produce_anchors
# from src.picture_config.config import picture_size

def draw_lists_of_strings(
    ax: Axes,
    xy: Tuple[float,float],
    width:float, 
    height:float,
    s_args:List[List[str]], 
    rel_str:List[float]=[2, 1],
    font_kwargs:List[dict]=[title_kwargs, label_kwargs],
    visible = False,
    **kwargs
    ):
    """ On axis ax, in the bounding box:
            xy, width, height : parameters same as in matplotlib.patches.Rectangle
        draw(use annotate) strings from:
            s_args = [ titles:List[string], labels_0:List[string], labels_1:labels_0, ...]
        with relative sizes:
            rel_str = [titles_size:float, labels_0_size:float , labels_1_size:float, ...]
        each with keyword arguments:
            font_kwargs = [titles_annotate_kwargs:dict, labels_0_annotate_kwargs:dict, ...].
        
        visible: bool Set the rectangles artist's visibility
        


    Strings from <s_args>[i] are drawn with:
            <rel_size>[i mod len(rel__size)] size
            <font_kwargs>[i mod len(font_kwargs)] font kwargs
        Use cell:
            import matplotlib.pyplot as plt
            from src.text.config import title_kwargs, label_kwargs
            fig, ax = plt.subplots()
            ax.set_facecolor('#393862')
            ax.set(xlim=(-0.05,3),ylim=(-0.05, 1.55))
            rel_str = [2, 1]
            titles, labels = ['Title is'], ['twice', 'as big as','labels here']
            s_args = [titles, labels]
            font_kwargs = [title_kwargs, label_kwargs]
            draw_lists_of_strings(ax, (0,1), 1, 0.5, s_args, rel_str, font_kwargs, visible=False)
            plt.show()
    """

    def get_scale(text:Annotation, rect:Rectangle):
        rect_Bbox:Bbox = rect.get_window_extent()
        text_Bbox:Bbox = text.get_window_extent()
        scale = min(rect_Bbox.height / text_Bbox.height,
                    rect_Bbox.width / text_Bbox.width)
        return scale
    # # sanity check:
    # main_bounding_box = Rectangle(xy = xy, width=width, height=height, 
    #                 fill=False, ec='r', lw=1 ,ls='--', visible=visible)
    # ax.add_patch(main_bounding_box)

    # draw from the top :
    start, stop = xy[1] + height, xy[1] # => anchors holding Y cordinates will have [greater , lesser] order
    assert len(s_args) == len(rel_str),\
        f"lengths of s_args (it is {len(s_args)}) should be same as rel_str (it is {len(rel_str)})"
    nums = list(map(len, s_args))
    anchors = produce_anchors(start, stop, rel_str=rel_str, nums=nums)
    for current_anchors, list_of_strings, text_kwargs in zip( anchors, s_args, font_kwargs):
        annotations = []
        scales = []
        for anchor, string in zip(current_anchors, list_of_strings):
            # print(f'string={string} between points {anchor}')
            box = Rectangle(xy = (xy[0], anchor[1]), width=width, height = abs(anchor[0]-anchor[1]), 
                    fill=False, ec=text_kwargs['color'], lw=0.5, ls='--', visible=visible)
            box = ax.add_patch(box)
            # text, xy, xytext=None, xycoords='data'
            annotation = ax.annotate(text=string, xy=(0,1), xytext=(0,1), xycoords=box, **text_kwargs)#,xy=(xy[0], anchor[0])
            annotations.append(annotation)
            scales.append(get_scale(annotation, box))
        scale = min(scales)
        for i in range(len(scales)):
            text:Annotation = annotations[i]
            text.set_fontsize(text.get_fontsize() * scale)
    return ax




#region Examples Experiments
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

# # string 'ABC' as patches :
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
#endregion