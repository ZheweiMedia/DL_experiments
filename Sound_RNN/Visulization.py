"""


visulize the sound.

visulize a folder. give the folder name.




"""

import sys
import glob
import os
import scipy.io.wavfile
import matplotlib.pyplot as plt


def main(argv):
    length_list = list()
    for sample in range(1,126):
        os.chdir('/home/medialab/Zhewei/data/Sound_Intonation/' + str(sample))
        for files in glob.glob('tang*.wav'):
            print (files)
            sound_array = scipy.io.wavfile.read(files)[1]
            length_list.append(len(sound_array))
            plt.plot(sound_array)
            plt.title(files)
            plt.show()
    print (length_list)
    print (max(length_list))

    plt.hist(length_list, 100)
    plt.xlabel('Length')
    plt.title('Histogram of the lengthes of the whole dataset')
    plt.show()













if __name__ == '__main__':
    main(sys.argv[1])
