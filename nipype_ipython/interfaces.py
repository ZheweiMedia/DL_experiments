"""
interfaces of Nipype

Zhewei@9/8/2016
"""

import numpy as np
import matplotlib.pyplot as plt
import nibabel as nib

def plot_slice(fname, z_idx=5):

    # Load the image and collect the data
    # and orientation information
    img = nib.load(fname)
    data = img.get_data()
    aff = img.get_affine()

    # Find the center of the brain matrix
    ctr = np.dot(np.linalg.inv(aff), [0, 0, 0, 1])[:3]

    # Plot the data
    vmin, vmax = (0, 1) if data.dtype == np.int16 else (30, 150)
    plt.imshow(np.rot90(data[:, :, ctr[2] + z_idx]), 
               cmap="gray", vmin=vmin, vmax=vmax)
    plt.gca().set_axis_off()

plot_slice("data/T1.nii.gz")
