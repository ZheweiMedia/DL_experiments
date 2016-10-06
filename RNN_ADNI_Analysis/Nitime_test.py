try:
    from nibabel import load
except ImportError:
    raise ImportError('You need nibabel (http:/nipy.org/nibabel/) in order to run this example')

import nitime.fmri.io as io
import os

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.mlab import csv2rec
import nitime

# Import the time-series objects:
from nitime.timeseries import TimeSeries

# Import the analysis objects:
from nitime.analysis import SpectralAnalyzer, FilterAnalyzer, NormalizationAnalyzer

TR = 1.35
f_lb = 0.02
f_ub = 0.15

data_file_path = test_dir_path = os.path.join(nitime.__path__[0],
                                              'data')

fmri_file = os.path.join(data_file_path, 'fmri1.nii.gz')

fmri_data = load(fmri_file)
volume_shape = fmri_data.shape[:-1]
coords = list(np.ndindex(volume_shape))
print (coords)
coords = np.array(coords).T

T_unfiltered = io.time_series_from_file(fmri_file,
                                        coords,
                                        TR=TR,
                                        normalize='percent')

T_fir = io.time_series_from_file(fmri_file,
                              coords,
                              TR=TR,
                              normalize='percent',
                              filter=dict(lb=f_lb,
                                          ub=f_ub,
                                          method='fir',
                                          filt_order=10))

T_iir = io.time_series_from_file(fmri_file,
                              coords,
                              TR=TR,
                              normalize='percent',
                              filter=dict(lb=f_lb,
                                          ub=f_ub,
                                          method='iir',
                                          filt_order=10))

T_boxcar = io.time_series_from_file(fmri_file,
                              coords,
                              TR=TR,
                              normalize='percent',
                              filter=dict(lb=f_lb,
                                          ub=f_ub,
                                          method='boxcar',
                                          filt_order=10))

fig05 = plt.figure()
ax05 = fig05.add_subplot(1, 1, 1)
S_unfiltered = SpectralAnalyzer(T_unfiltered).spectrum_multi_taper
S_fir = SpectralAnalyzer(T_fir).spectrum_multi_taper
S_iir = SpectralAnalyzer(T_iir).spectrum_multi_taper
S_boxcar = SpectralAnalyzer(T_boxcar).spectrum_multi_taper

random_voxel = np.random.randint(0, np.prod(volume_shape))

ax05.plot(S_unfiltered[0], S_unfiltered[1][random_voxel], label='Unfiltered')
ax05.plot(S_fir[0], S_fir[1][random_voxel], label='FIR filtered')
ax05.plot(S_iir[0], S_iir[1][random_voxel], label='IIR filtered')
ax05.plot(S_boxcar[0], S_boxcar[1][random_voxel], label='Boxcar filtered')
ax05.legend()
plt.show()
