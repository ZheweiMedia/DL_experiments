"""
Get more fMRI data, other than just the first visit in data_analysis.py

"""



def main():

    import csv
    with open('idaSearch_2_29_2016.csv','rb') as csvfile:
        reader = csv.DictReader(csvfile)
        wholeData = []
        for row in reader:
            wholeData.append(row)

    AD_imageID = list()
    NC_imageID = list()
    EMCI_imageID = list()
    SMC_imageID = list()
    LMCI_imageID = list()
    MCI_imageID = list()
    for row in wholeData:
        if row['DX Group'] == 'AD' and row['Description'] == 'Resting State fMRI':
            AD_imageID.append(row['Image ID'])
            pass
        if row['DX Group'] == 'Normal' and row['Description'] == 'Resting State fMRI':
            NC_imageID.append(row['Image ID'])
            pass
        if row['DX Group'] == 'LMCI' and row['Description'] == 'Resting State fMRI':
            LMCI_imageID.append(row['Image ID'])
            pass
        if row['DX Group'] == 'SMC' and row['Description'] == 'Resting State fMRI':
            SMC_imageID.append(row['Image ID'])
            pass
        if row['DX Group'] == 'MCI' and row['Description'] == 'Resting State fMRI':
            MCI_imageID.append(row['Image ID'])
            pass
        if row['DX Group'] == 'EMCI' and row['Description'] == 'Resting State fMRI':
            EMCI_imageID.append(row['Image ID'])
            pass
        
    f = open('Whole_AD_NC.txt', 'w')
    f.write('AD:\n')
    for sampleNo, sample in enumerate(AD_imageID):
        f.write(sample)
        f.write(' ')
        if (sampleNo+1)%5 == 0:
            f.write('\n')
            
    f.write('\n'*3)       
    f.write('NC:\n')
    for sampleNo, sample in enumerate(NC_imageID):
        f.write(sample)
        f.write(' ')
        if (sampleNo+1)%5 == 0:
            f.write('\n')
            
    f.write('\n'*3)       
    f.write('MCI:\n')
    for sampleNo, sample in enumerate(MCI_imageID):
        f.write(sample)
        f.write(' ')
        if (sampleNo+1)%5 == 0:
            f.write('\n')
            
    f.write('\n'*3)       
    f.write('EMCI:\n')
    for sampleNo, sample in enumerate(EMCI_imageID):
        f.write(sample)
        f.write(' ')
        if (sampleNo+1)%5 == 0:
            f.write('\n')
    
    f.write('\n'*3)       
    f.write('LMCI:\n')
    for sampleNo, sample in enumerate(LMCI_imageID):
        f.write(sample)
        f.write(' ')
        if (sampleNo+1)%5 == 0:
            f.write('\n')
            
    f.write('\n'*3)       
    f.write('SMCI:\n')
    for sampleNo, sample in enumerate(SMC_imageID):
        f.write(sample)
        f.write(' ')
        if (sampleNo+1)%5 == 0:
            f.write('\n')
            
        
        





























if __name__ == '__main__':
    main()
