"""
test slcie timing

Zhewei@9/8/2016
"""

from nipype.interfaces.spm import SliceTiming
st = SliceTiming()
st.inputs.in_files = 'ADNI_136_S_4993_MR_Resting_State_fMRI_br_raw_20121025152216163_2750_S172266_I342514.nii'
st.inputs.num_slices = 48
st.inputs.time_repetition = 3
st.inputs.time_acquisition = 3-3/48
st.inputs.slice_order = list(range(48,0,-1))
st.inputs.ref_slice = 1
st.run()
