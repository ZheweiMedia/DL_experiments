"""

nipype warped spm

"""

import sys
import nipype.interfaces.spm as spm

norm12 = spm.Normalize12()
norm12.inputs.image_to_align = sys.argv[1]
norm12.inputs.apply_to_files = sys.argv[2:]
norm12.inputs.write_bounding_box = [[-90, -126, -72], [90, 90, 108]]
norm12.run()


# the end
