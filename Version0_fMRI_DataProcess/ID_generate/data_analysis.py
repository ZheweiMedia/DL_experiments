'''
used for analysis .csv file of ADNI

'''

def main():

    import csv
    with open('idaSearch_2_29_2016.csv','rb') as csvfile:
        reader = csv.DictReader(csvfile)
        wholeData = []
        for row in reader:
            wholeData.append(row)

    # find out the Image ID of a subject which has fMRI, MP-RAGE,
    # MP-RAGE(processed), MPRAGE Sense2, MPRAGE sense2(processed) at the same time
    # If this happens many times, only ouput the first time
    conditions = ['fMRI','MP_RAGE','MP_RAGE_Process','MP_RAGE_S2','MP_RAGE_S2_Process']
    for i in conditions:
        i_JUDGE = i+'_JUDGE'
        i_ID = i+'_ID'
        _JUDGE = {'flag':0,'Image ID':0}
        _ID = []
        exec(i_JUDGE+'=_JUDGE') in locals()
        exec(i_ID+'=_ID') in locals()


    First_time_Flag = 1
    EXIST_Flag = 0
    Subject_ID = wholeData[0]['Subject ID']
    Age = wholeData[0]['Age']

    for row in wholeData:
        if row['Subject ID'] == Subject_ID and row['Age'] == Age:
            if EXIST_Flag ==1:
                pass
            else:
                UpdateJudge(row,fMRI_JUDGE,MP_RAGE_JUDGE,MP_RAGE_Process_JUDGE,\
                                    MP_RAGE_S2_JUDGE,MP_RAGE_S2_Process_JUDGE)

                if fMRI_JUDGE['flag'] and MP_RAGE_JUDGE['flag'] and MP_RAGE_Process_JUDGE['flag']\
                            and MP_RAGE_S2_JUDGE['flag'] and MP_RAGE_S2_Process_JUDGE['flag'] == 1:
                    EXIST_Flag = 1
                    fMRI_ID.append({'Image ID':fMRI_JUDGE['Image ID'],'DX Group':fMRI_JUDGE['DX Group']})
                    MP_RAGE_ID.append({'Image ID':MP_RAGE_JUDGE['Image ID'],'DX Group':MP_RAGE_JUDGE['DX Group']})
                    MP_RAGE_Process_ID.append({'Image ID':MP_RAGE_Process_JUDGE['Image ID'],\
                                                    'DX Group':MP_RAGE_Process_JUDGE['DX Group']})
                    MP_RAGE_S2_ID.append({'Image ID':MP_RAGE_S2_JUDGE['Image ID'],\
                                            'DX Group':MP_RAGE_S2_JUDGE['DX Group']})
                    MP_RAGE_S2_Process_ID.append({'Image ID':MP_RAGE_S2_Process_JUDGE['Image ID'],\
                                                    'DX Group':MP_RAGE_S2_Process_JUDGE['DX Group']})
                    initial(fMRI_JUDGE,MP_RAGE_JUDGE,MP_RAGE_Process_JUDGE,\
                                        MP_RAGE_S2_JUDGE,MP_RAGE_S2_Process_JUDGE)

        if row['Subject ID'] == Subject_ID  and  row['Age'] != Age:
            Age = row['Age']
            initial(fMRI_JUDGE,MP_RAGE_JUDGE,MP_RAGE_Process_JUDGE,\
                                MP_RAGE_S2_JUDGE,MP_RAGE_S2_Process_JUDGE)
            if EXIST_Flag ==1:
                pass
            else:
                UpdateJudge(row,fMRI_JUDGE,MP_RAGE_JUDGE,MP_RAGE_Process_JUDGE,\
                                    MP_RAGE_S2_JUDGE,MP_RAGE_S2_Process_JUDGE)
        if row['Subject ID'] != Subject_ID:
            Subject_ID = row['Subject ID']
            Age = row['Age']
            EXIST_Flag = 0
            initial(fMRI_JUDGE,MP_RAGE_JUDGE,MP_RAGE_Process_JUDGE,\
                                MP_RAGE_S2_JUDGE,MP_RAGE_S2_Process_JUDGE)
            UpdateJudge(row,fMRI_JUDGE,MP_RAGE_JUDGE,MP_RAGE_Process_JUDGE,\
                                MP_RAGE_S2_JUDGE,MP_RAGE_S2_Process_JUDGE)

    f = open('results.txt', 'w')
    deleteFileContent(f)
    labels = []
    for no in range(len(fMRI_ID)):
        labels.append(fMRI_ID[no]['DX Group'])
    labels = list(set(labels))
    for labelName in labels:
        f.write(labelName)
        f.write(' : ======================================================')
        f.write('\n')
        for imagetype in conditions:
            f.write( imagetype+' Image ID is :')
            f.write('\n')
            imType = locals()[imagetype+'_ID']
            printtimes = 0
            for i in range(len(fMRI_ID)):
                if fMRI_ID[i]['DX Group'] == labelName:
                    printtimes += 1
                    f.write(imType[i]['Image ID'])
                    f.write(' ')
                    if printtimes%5 == 0:
                        f.write('\n')
            f.write('\n')




def initial(fMRI_JUDGE,MP_RAGE_JUDGE,MP_RAGE_Process_JUDGE,\
                    MP_RAGE_S2_JUDGE,MP_RAGE_S2_Process_JUDGE):
    # inital values to 0. for new judge begin
    fMRI_JUDGE['flag'] = 0
    MP_RAGE_JUDGE['flag'] = 0
    MP_RAGE_Process_JUDGE['flag'] = 0
    MP_RAGE_S2_JUDGE['flag'] = 0
    MP_RAGE_S2_Process_JUDGE['flag'] = 0

def UpdateJudge(row,fMRI_JUDGE,MP_RAGE_JUDGE,MP_RAGE_Process_JUDGE,\
                    MP_RAGE_S2_JUDGE,MP_RAGE_S2_Process_JUDGE):
    #
    if row['Description'] == 'Resting State fMRI':
        fMRI_JUDGE['flag'] = 1
        fMRI_JUDGE['Image ID'] = row['Image ID']
        fMRI_JUDGE['DX Group'] = row['DX Group']
    if row['Description'] == 'MPRAGE':
        MP_RAGE_JUDGE['flag'] = 1
        MP_RAGE_JUDGE['Image ID'] = row['Image ID']
        MP_RAGE_JUDGE['DX Group'] = row['DX Group']
    if row['Description'] == 'MT1; N3m <- MPRAGE':
        MP_RAGE_Process_JUDGE['flag'] = 1
        MP_RAGE_Process_JUDGE['Image ID'] = row['Image ID']
        MP_RAGE_Process_JUDGE['DX Group'] = row['DX Group']
    if row['Description'] == 'MPRAGE SENSE2':
        MP_RAGE_S2_JUDGE['flag'] = 1
        MP_RAGE_S2_JUDGE['Image ID'] = row['Image ID']
        MP_RAGE_S2_JUDGE['DX Group'] = row['DX Group']
    if row['Description'] == 'MT1; N3m <- MPRAGE SENSE2':
        MP_RAGE_S2_Process_JUDGE['flag'] = 1
        MP_RAGE_S2_Process_JUDGE['Image ID'] = row['Image ID']
        MP_RAGE_S2_Process_JUDGE['DX Group'] = row['DX Group']


def deleteFileContent(fileName):
    fileName.seek(0)
    fileName.truncate()




if __name__ == '__main__':
    main()
