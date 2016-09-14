"""
Configurable Pipeline for the Analysis of Connectomes
=====================================================

CPAC is a configurable, open-source, Nipype-based, automated processing pipeline for resting state functional MRI (R-fMRI) data, for use by both novice and expert users.
"""

import numpy as np
import pyximport
pyximport.install(setup_args={'include_dirs': [np.get_include()]})

from numpy.testing import nosetester
test = nosetester.NoseTester.test

class _NoseTester(nosetester.NoseTester):
    def test(self, label='fast', verbose=1, extra_argv=['--exe'], doctests = False, coverage=False):
        return super(_NoseTester, self).test(label=label, verbose=verbose, extra_argv=extra_argv, doctests=doctests, coverage=coverage)

test = _NoseTester().test

from CPAC.reho import reho
from CPAC.func_preproc import func_preproc
from CPAC.seg_preproc import seg_preproc
from CPAC.registration import registration
from CPAC.sca import sca
from CPAC.basc import basc
from CPAC.nuisance import nuisance
from CPAC.generate_motion_statistics import generate_motion_statistics
from CPAC.alff import alff
from CPAC.qc import qc
from CPAC.seg_preproc import seg_preproc
from CPAC.vmhc import vmhc
from CPAC.median_angle import median_angle
from CPAC.timeseries import timeseries_analysis
from CPAC.network_centrality import core
from CPAC.network_centrality import resting_state_centrality
from CPAC.network_centrality import utils
from CPAC.scrubbing import scrubbing
from CPAC.group_analysis import group_analysis
from CPAC.easy_thresh import easy_thresh
from CPAC.utils import utils
from CPAC.pipeline import *
from CPAC.cwas import cwas
from CPAC.GUI import *
from CPAC.anat_preproc import anat_preproc




__all__ = ['GUI', 'pipeline', 'anat_preproc', 'func_preproc', 'registration', 'seg_preproc', 'reho', 'sca', 'basc', 'nuisance', 'alff', 'vmhc', 'median_angle', 'generate_motion_statistics', 'timeseries', 'network_centrality', 'scrubbing', 'utils', 'group_analysis', 'easy_thresh', 'qc', 'cwas']

from subprocess import Popen, PIPE
import re
#__version__ = '0.1-git'

try:
    version = '0.3.9.2'


#    gitproc = Popen(['git', 'log', '--oneline'], stdout = PIPE)
#    (stdout, stderr) = gitproc.communicate()
#    rows = stdout.split("\n")
#    v_num = re.search( r'(?<=(version_|release_))(.)*', rows[0])
#    if v_num:
#        version = v_num.group(0).strip("'")
#    else:
#        version = 'unknown_version'
except OSError:
    version = 'unknown_version'

__version__ =  str(version)
