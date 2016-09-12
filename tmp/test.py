"""
test slcie timing

Zhewei@9/8/2016
"""
import fnmatch, re
from nipype.interfaces.spm import SliceTiming
st = SliceTiming()
st.inputs.in_files =['20120201_084246RestingStatefMRIs601a1006_010.nii','20120201_084246RestingStatefMRIs601a1006_015.nii']
st.inputs.num_slices = 48
st.inputs.time_repetition = 3
st.inputs.time_acquisition = 3-3/48
st.inputs.slice_order = list(range(0,48,1))
st.inputs.ref_slice = 24
st.run()
