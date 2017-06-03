import numpy as np
from mayavi import mlab
import pickle
import gzip

with open('wholeresult.tar.gz', 'r') as out_file:
    results = pickle.load(out_file)

print len(results)

tmp = results[0]


x, y, z = np.ogrid[0:tmp.shape[0], 0:tmp.shape[1], 0:tmp.shape[2]]
s = tmp[x,y,z]

src = mlab.pipeline.scalar_field(s)
mlab.pipeline.iso_surface(src, contours=[s.min()+0.1*s.ptp(), ])

mlab.show()
