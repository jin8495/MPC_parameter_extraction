import numpy as np

from numba import njit
from numba.typed import List

from src.const import *

# get dataset witout allzero
def get_data(dataset_path, remove_allzeros=True):
    data = np.load(dataset_path).astype(np.uint8)

    @njit
    def exclude_all_word_same(data):
        new_data = List()
        for d in data:
            if not((d[0::4]==d[0] and d[1::4]==d[1] and d[2::4]==d[2] and d[3::4]==d[3]).all()):
                new_data.append(d)
        return new_data

    # exclude all-zeros lines
    if (remove_allzeros):
        non_zero_indices = np.where(data.any(axis=1))[0]
        data = data[non_zero_indices]

    # exclude all-word same lines
    if (remove_allwordsame):
        data = list(exclude_all_word_same(data))

    return data

# get dataset without allzero
# and labels #0 for all-zeros #1 for others
def get_data_and_label(dataset_path, label_path):
    """
    Before:
        Bool            = 0,
        Char            = 1,
        Short           = 2,
        Int             = 3,
        Long            = 4,
        Float           = 5,
        Double          = 6
    After:
        All-Zeros       = 0,
        All-WordSame    = 1,
        Bool/Char       = 2,
        Short           = 3,
        Int/Long        = 4,
        Float           = 5,
        Double          = 6,
        Uncomp          = 7
    """
    data = np.load(dataset_path).astype(np.uint8)
    labels = np.load(label_path)

    @njit
    def get_labels(data, labels):
        new_labels = List()
        for i, d in enumerate(data):
            # all-zero
            if (d == 0).all():
                new_labels.append(0)
            # all-wordsame
            elif ((d[0::4]==d[0]).all()
                and (d[1::4]==d[1]).all()
                and (d[2::4]==d[2]).all()
                and (d[3::4]==d[3]).all()):
                new_labels.append(1)
            # bool/char
            elif (labels[i]==0 or labels[i]==1):
                new_labels.append(2)
            # short
            elif (labels[i]==2):
                new_labels.append(3)
            # int/long
            elif (labels[i]==3 or labels[i]==4):
                new_labels.append(4)
            # float
            elif (labels[i]==5):
                new_labels.append(5)
            # double
            elif (labels[i]==6):
                new_labels.append(6)
            else:
                assert(False, "Cannot enter this branch")
        return new_labels
    labels = np.array(get_labels(data, labels))
    return data, labels

def sort_lines_by_class(data, labels):
    data_classes = {}
    for selected_class in range(NUM_FIRST_CLUSTER, NUM_CLUSTERS - 1):
        print("Sorting class #%2d / %d..." %(selected_class, NUM_CLUSTERS), end='\r')
        data_classes[selected_class] = data[labels == selected_class]
    print()

# @njit
# def sort_lines_numba(lines, labels, selected_labels):
#     sorted_lines = List()
#     for idx, line in enumerate(lines):
#         if(labels[idx] == selected_labels):
#             sorted_lines.append(line)
#     return list(sorted_lines)

