import numpy as np
from typing import List

#### Relative division of (0,1) helper functions:
def relative_01_group_dividers(relative_sizes:List[float], num_in_group:List[int]):
    """ Return endpoints of queues of equal length intervals in (0, 1).
        Assume len(relative_sizes) == len(relative_sizes)
        """
    strength = np.array(relative_sizes)
    number = np.array(num_in_group)

    total  = (strength * number).sum()
    ratios = (strength * number) / total
    return np.cumsum(np.hstack(([0], ratios)))

def produce_intervals(arr: np.array):
    """split array of increasing numbers into array of pairs of consecutive points"""
    starts  = arr[:-1]
    ends    = arr[1:]
    return np.array([[a,b] for a,b in zip(starts, ends)])

def equal_divide_of(interval_list, into_this_many):
    """ Divide interval_list[i] into into_this_many[i] points"""
    ziped = zip(interval_list, into_this_many)
    return [np.linspace(*interval, n+1) for interval, n in ziped]

#### main
def produce_anchors(start: float, stop: float, rel_str: List[float], nums: List[int]):
    """ Return partition of interval (start, stop) into queue of queues of intervals.
        Intervals in each queue are of equal length and do not overlap.
        There are len(nums) queues with nums[i] intervals in i-th queue.
        In total there are sum(nums) intervals.
        If length_<i> denotes length of a interval belonging to <i>-th queue then
            length_i/length_j == rel_str[i]/rel_str[j]
        is fulfilled.

        Example cell:
            import numpy as np
            import matplotlib.pyplot as plt

            from src.text.text_anchors import produce_anchors
            number_of_points = [1, 2, 1, 3, 1]
            relative_weight = [5, 2, 5, 1, 5]
            start, stop = 0, 1
            anchors = produce_anchors(start, stop, relative_weight, number_of_points)
            # for integer relative weights line below yields true integer labels for relative partition
            labels = np.round(y*sum(np.array(relative_weight)*np.array(number_of_points))).astype(int)

            pts = np.vstack(anchors)
            y = np.hstack(tup=(pts[:,0], pts[-1,-1]))
            x = np.linspace(0,1,len(y))

            eps = 0.05
            fig, ax = plt.subplots()
            ax.set(xlim=(0-eps,1+eps), ylim=(0-eps,1+eps), aspect='equal')
            ax.hlines(y, xmin=0, xmax=1, colors='k', lw=0.5)
            ax.vlines([0,1], ymin=0, ymax=1, colors='k', lw=0.5)
            ax.set_yticks(ticks=y,labels=labels)
            ax.set_xticks(ticks=[0,1])
            plt.show()
                """
    # Relative division of (0,1) interval:
    rel_01_dividers =  relative_01_group_dividers(rel_str, nums)
    intervals_to_divide = produce_intervals(rel_01_dividers)
    intervals_divided = equal_divide_of(intervals_to_divide, nums)
    result_01 = list(map(produce_intervals, intervals_divided))

    # scaling to (start, stop) 
    result_XY = list(map(
        lambda arr : start + (stop-start)*arr,
        result_01
    ))
    return result_XY