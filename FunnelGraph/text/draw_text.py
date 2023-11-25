import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from matplotlib.axes import Axes
from matplotlib.text import Annotation
from matplotlib.transforms import Bbox

from typing import List, Tuple

from text.config import title_kwargs, label_kwargs
from text.text_anchors import produce_anchors
# from graph.picture_config.config import picture_size

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

    Example cell:
        import matplotlib.pyplot as plt
        from text.config import title_kwargs, label_kwargs
        from text.draw_text import draw_lists_of_strings

        fig, ax = plt.subplots()
        ax.set_facecolor('#393862')
        ax.set(xlim=(-0.05, 5), ylim=(-0.05, 1.55))

        xy = (0.5, 0.6)
        width, height = 2.5, 0.6
        rel_str = [2, 1]
        titles, labels = ['Title is'], ['twice', 'as big as','labels here']
        s_args = [titles, labels]
        font_kwargs = [title_kwargs, label_kwargs]

        draw_lists_of_strings(
            ax=ax, xy=xy, width=width, height=height, 
            s_args=s_args, rel_str=rel_str, 
            font_kwargs=font_kwargs, visible=True)
        plt.show()
    """

    def get_scale(text:Annotation, rect:Rectangle):
        rect_Bbox:Bbox = rect.get_window_extent()
        text_Bbox:Bbox = text.get_window_extent()
        scale = min(rect_Bbox.height / text_Bbox.height,
                    rect_Bbox.width / text_Bbox.width)
        return scale
    
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