import numpy as np
import matplotlib.cbook as cbook


def save_npz(npz_filename, x, y):
    np.savez(npz_filename, x, y)
