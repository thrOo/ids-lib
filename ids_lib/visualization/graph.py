import numpy as np
import matplotlib.pyplot as plt

from ids_lib.helpers.parse_npz import parse_npz


def PrettyGraph(title, x_label, y_label, datas):
    # Load a numpy record array from yahoo csv data with fields date, open, close,
    # volume, adj_close from the mpl-data/example directory. The record array
    # stores the date as an np.datetime64 with a day unit ('D') in the date column.
    #with cbook.get_sample_data('goog.npz') as datafile:
    #   price_data = np.load(datafile)['price_data'].view(np.recarray)
    fig, ax = plt.subplots()

    for i, data in enumerate(datas):
        names = data[:, 0]
        x = data [:, 1]
        y = data [: , -1]
        s = [250 for n in range(len(x))]
        ax.scatter(x, y, alpha=0.5 , s=s)
        for i, txt in enumerate(names):
            ax.annotate(str(int(txt)), (x[i], y[i]), textcoords="offset points", xytext=(0,-4), ha='center', fontsize=10)

    ax.set_xlabel(x_label, fontsize=15)
    ax.set_ylabel(y_label, fontsize=15)
    ax.set_title(title)

    ax.grid(True)
    fig.tight_layout()

    plt.show()


