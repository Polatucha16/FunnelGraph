import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

from abc import ABC, abstractmethod
from typing import List

from src.text.config import text_stage_kwargs, text_nums_kwargs
from src.pic_config.config import pic_global

class ColumnPrintStrategy(ABC):
    @abstractmethod
    def prepare_string_list(self, list: List[str]) -> List[str]:
        pass


class JustNumbers(ColumnPrintStrategy):
    def prepare_string_list(self, list: List[str]) -> List[str]:
        for i in range(len(list)):
            list[i] = list[i].rjust(4)
        return list


class WithPercent(ColumnPrintStrategy):
    def prepare_string_list(self, list: List[str]) -> List[str]:
        for i in range(len(list)):
            list[i] = (list[i] + " %").rjust(6)
        return list


def label_stage(
    ax: plt.Axes,
    stage: int,
    label: str,
    column_print_strategy: ColumnPrintStrategy,
    number_column: np.ndarray,
    apply_colorQ: bool,
    cmap_list: list,
    cmap_arg: float,
):
    """Function puts labels and numbers to the stage,
    cell example using label_stage:

        import numpy as np
        import matplotlib.pyplot as plt

        from src.funel_graph import FunelGraph
        from src.text.text import JustNumbers, WithPercent
        from src.text.text import label_stage

        fg = FunelGraph()
        fg.prepare()
        fg.set_colors()


        fig, ax = plt.subplots()

        ax.set_facecolor('#393862')
        plt.xlim(0, 2)
        plt.ylim(0, 1.5)
        label_stage(
            ax=ax,
            stage=0,
            label='Matplotlib',
            column_print_strategy=JustNumbers(),
            number_column=np.array([34,27,11,12]),
            apply_colorQ= True,
            cmap_list=fg.data_dict['colors'],
            cmap_arg=0)
        plt.show()
    """

    # box for text

    x0, y0 = stage * pic_global["stage_width"], pic_global["funnel_height"]
    x1, y1 = (stage + 1) * pic_global["stage_width"], pic_global["picture_height"]
    width, height = x1 - x0, y1 - y0
    box = Rectangle((x0, y0), width, height, fc="none", ec="none")
    ax.add_patch(box)

    # drawing top label
    label_gaps = {"box_gap": 0.02, "first_no_XY": (0, 0)}
    gap = label_gaps["box_gap"]
    text = ax.text(x0 + gap, y1 - gap, label, **text_stage_kwargs)

    # the column of numbers
    string_list = np.char.mod("%d", number_column).tolist()
    strings_to_annotate = column_print_strategy.prepare_string_list(string_list)

    colors_at_stage_reversed = list(cmap_list.__reversed__())
    default_num_color = text_nums_kwargs["color"]

    for i, num_str in enumerate(strings_to_annotate):
        if apply_colorQ == True:
            text_nums_kwargs["color"] = colors_at_stage_reversed[i](cmap_arg)
        text = ax.annotate(
            num_str,
            xycoords=text,
            xy=label_gaps["first_no_XY"] if i == 0 else (1, 0),
            va="top",
            ha="left" if i == 0 else "right",
            **text_nums_kwargs
        )
    text_nums_kwargs["color"] = default_num_color

    return text
