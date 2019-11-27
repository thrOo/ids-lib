import numpy as np
import matplotlib.cbook as cbook


def parse_npz(npz_filename, field_name):
    with cbook.get_sample_data(npz_filename) as datafile:
        values = np.load(datafile)[field_name].view(np.recarray)
        return values
