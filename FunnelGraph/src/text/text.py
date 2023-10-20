import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

from src.text.config import text_stage_kwargs, text_nums_kwargs
from src.pic_config.config import pic_global

def label_stage(ax: plt.Axes, stage:int, label:str, number_column:np.ndarray, cmap_list:list):
    """ Function to add text to stage example for jupyter:

        import matplotlib.pyplot as plt
        from matplotlib.patches import Rectangle

        # plt.rcParams["font.size"] = 20
        fig, ax = plt.subplots()

        ax.set_facecolor('#393862')
        plt.xlim(0, 2)
        plt.ylim(0, 1.5)

        ax.set_aspect('equal')

        title_dict = dict(
            size=20,
            color="tab:orange",
            va='top', ha='left',
            family='sans-serif',
            weight="bold", 
            )
        numbs_dict = dict(
            size=20,
            color='#e3dac9', 
            weight='bold', 
            family='sans-serif'
            )
        x0, y0, x1, y1 = 0.0, 1, 1, 1.5
        width, height = x1 - x0, y1 - y0
        rect = Rectangle((x0, y0), width, height, fc="none", ec='y')#, ec="none")
        ax.add_patch(rect)

        gap = 0.02
        text = ax.text(x0+gap, y1-gap, "Matplotlib", **title_dict)

        text = ax.annotate(
            "34 %", xycoords=text, xy=(0.05, -0.5), va="top", ha='left', **numbs_dict)
        text = ax.annotate(
            "27 %", xycoords=text, xy=(1, 0), va="top", ha='right', **numbs_dict)
        text = ax.annotate(
            "11 %", xycoords=text, xy=(1, 0), va="top",ha='right', **numbs_dict)
        plt.show()
    """

    # box for text
    x0, y0, = stage * pic_global['stage_width'], pic_global['funnel_height'],
    x1, y1 = (stage+1) * pic_global['stage_width'], pic_global['picture_height']
    width, height = x1 - x0, y1 - y0
    box = Rectangle((x0, y0), width, height, fc="none", ec="none")
    ax.add_patch(box)
    
    # drawing top label
    label_gaps = {'box_gap' : 0.02, 
                  'first_no_XY' : (0, 0)
                  }
    gap = label_gaps['box_gap']
    text = ax.text(x0+gap, y1-gap, label, **text_stage_kwargs)

    # first stage there are no % sign
    if stage != 0:
        # rest of the stages have bone color
        text_nums_kwargs['color'] = '#e3dac9'
        for i, num in enumerate(number_column):
            if i == 0:
                xy = label_gaps['first_no_XY']
                text = ax.annotate(str(num).rjust(4)+" %", xycoords=text, xy=xy, 
                                va="top", ha='left', **text_nums_kwargs)
            else:
                text = ax.annotate(str(num).rjust(4)+" %", xycoords=text, xy=(1, 0), 
                                va="top", ha='right', **text_nums_kwargs)
    # rest of the stages have % of the previous
    elif stage == 0:
        # stage 0 overwrite colors
        colors_at_zero_reversed = list(cmap_list.__reversed__())

        for i, num in enumerate(number_column):
            if i == 0:
                xy = label_gaps['first_no_XY']
                text_nums_kwargs['color'] = colors_at_zero_reversed[i](0)
                text = ax.annotate(str(num).rjust(4), xycoords=text, xy=xy, 
                                va="top", ha='left', **text_nums_kwargs)
            else:
                text_nums_kwargs['color'] = colors_at_zero_reversed[i](0)
                text = ax.annotate(str(num).rjust(4), xycoords=text, xy=(1, 0), 
                                va="top", ha='right', **text_nums_kwargs)
    return text