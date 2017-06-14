"""

nipype warped spm for coregistration

"""

import sys
import nipype.interfaces.spm as spm

coreg = spm.Coregister()
coreg.inputs.target = sys.argv[1]
coreg.inputs.source = sys.argv[2]
coreg.run()


# the end
