"""




"""


from processData import readfile
import gzip, pickle, numpy
import nibabel as nib

url = '/home/medialab/Zhewei/MICCAI_Les_2017_Process/Unet_3D/'

trainlinks, trainannotlinks, testlinks, testannotlinks = readfile(url+'link/UnetSample_train.txt',\
                                                                url+'link/UnetLabel_train.txt', \
                                                                url+'link/UnetSample_test.txt', \
                                                                url+'link/UnetLabel_test.txt')

print (len(testannotlinks))

for iNo, i in enumerate(testannotlinks):
    with gzip.open(i,'r') as gtfile:
        gt = pickle.load(gtfile)
        gt = gt.reshape((gt.shape[0], gt.shape[1], gt.shape[2], 1))
        gtimg = nib.Nifti1Image(gt, numpy.eye(4))
    with gzip.open('/home/medialab/Zhewei/MICCAI_Les_2017_Process/data/predict/'+str(iNo)+'.tar.gz', 'r') as predfile:
        pred = pickle.load(predfile).astype(float)
        pred = pred.reshape((pred.shape[0],pred.shape[1], pred.shape[2], 1))
        predimg = nib.Nifti1Image(pred, numpy.eye(4))

    nib.save(gtimg, '/home/medialab/Zhewei/MICCAI_Les_2017_Process/data/compare/gt'+str(iNo)+'.nii.gz')
    nib.save(predimg, '/home/medialab/Zhewei/MICCAI_Les_2017_Process/data/compare/pred'+str(iNo)+'.nii.gz')
    print (iNo, numpy.sum(gt), numpy.sum(pred))
