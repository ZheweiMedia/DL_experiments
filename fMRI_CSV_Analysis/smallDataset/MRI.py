"""




"""

import gzip
import pickle
import os
from glob import glob

os.chdir('/home/medialab/data/tmp')

fMRI_ID = list()
for i in glob('*/'):
    print (i)
    print (i[5:11])
    fMRI_ID.append(i[5:11])

print (len(fMRI_ID))

os.chdir('/home/medialab/Zhewei/fMRI_CSV_Analysis/smallDataset')

with gzip.open("smallDataset_fMRIList", "wb") as output_file:
    pickle.dump(fMRI_ID, output_file)


badDataList = ['224706', '196079', '223981']

with open('fMRI_ID', 'w') as output_file:
    for ID in fMRI_ID:
        if ID not in badDataList:
            output_file.write(ID)
            output_file.write('\n')
