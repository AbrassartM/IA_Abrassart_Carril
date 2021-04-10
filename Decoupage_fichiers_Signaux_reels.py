import pylab as plt
import numpy as np
import h5py as h5
import os
import os.path as osp
from scipy import signal


def decoupage_BDD(sig, mems, path):
    """
    function decoupage_BDD
    Découpe un fichier .h5 de la BDD en des spectrogrammes de
    chacun une seconde

    in:
    sig : (str) nom du fichier .h5 dans la BDD
    mems : (int) numéro du micro choisi
    path : (str) chemin par lequel on accède aux fichiers .h5

    out : 
    figures
    figures enregistrées au format .png
    """
    home = os.environ["HOMEPATH"]
    path_data = osp.join(home,path)
    filename = osp.join(path_data, sig)
    with h5.File(filename, 'r') as h5file:
        x = h5file["Mems"+str(mems)][...]
    fs = int(5e4)
    dur = len(x)//fs
    
    x_2 = np.reshape(x,(len(x)//fs,fs))
    for i in range(0,len(x_2[:,0])):
        var = i
        var = plt.figure()
        f, t, Sxx = signal.spectrogram(x_2[i,:], fs, nperseg=2048)
        Sxx_2 = Sxx[0 : len(Sxx[:,0])//5 , :]
        Sxx_3 = np.zeros((len(Sxx_2[:,0])//5, len(Sxx_2[0,:])))
        for i in range(0,len(Sxx_3[:,0])):
            Sxx_3[i,:] = np.mean(Sxx_2[5*i : 5*(i+1) , :], axis = 0)
        plt.pcolormesh(Sxx_3, shading='gouraud')
        plt.title(sig), plt.ylabel('F en Hz'), plt.xlabel('1 seconde')
        nom = sig
        nom = nom[0 : len(sig)-3]
        var.savefig(nom + str(mems) + str(i+1) + '.png')

        

