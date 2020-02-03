import os
import json
import uuid
from PIL import Image
import requests

import matplotlib
import matplotlib.pyplot as plt

plt.ioff()
matplotlib.rcParams.update({'figure.max_open_warning': 0})


def ic_auto_exclude(ica, verbose=False):
    ic_to_reject = []
    for i in range(ica.n_components_):
        plot_to_save = ica.plot_components(i, show=False)
        plot_filename = str(uuid.uuid4()) + ".png"
        plot_to_save.savefig(plot_filename)

        # cropping images
        plot_to_save = Image.open(plot_filename)
        plot_to_save = plot_to_save.crop((25, 56, 205, 232))
        plot_to_save.save(plot_filename)

        img = open(plot_filename, 'rb')
        files = {'plot': (plot_filename, img, 'image/png')}
        resp = requests.post('http://icamark.herokuapp.com/label', files=files).text
        label = json.loads(resp)['label']
        if label == 0:
            ic_to_reject.append(i)
        os.remove(plot_filename)
        if verbose:
            print("ICA#{} ({})".format(i, label))
    return ic_to_reject
