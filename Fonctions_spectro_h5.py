#!/usr/bin/env python
# coding: utf-8

# In[ ]:


def get_signal(filename, mems):
    """
    Function get_signal
    Récupère un signal .h5 selon son nom et le numéro du micro voulu
    
    in : 
    filename : (str) nom du fichier à récupérer
    mems : (int) numéro du micro voulu
    
    out : 
    x : (np.array(float)) signal extrait
    """
    with h5.File(filename, 'r') as h5file:
        x = h5file["Mems"+str(mems)][...]
    return x
    
def spectro_gouraud(filename,mems):
    """
    Function spectro_gouraud
    Crée un spectrogramme avec la fonction pcolormesh
    à partir d'un fichier .h5 spécifié et son numéro de
    micro voulu
    
    in : 
    filename : (str) nom du fichier à récupérer
    mems : (int) numéro du micro voulu
    
    out : 
    t : (np.array(float)) axe des abscisses en secondes
    f : (np.array(float)) axe des ordonnées en Hz
    Sxx : (np.array((float, float))) matrice spectrogramme
    """
    fs = int(5e4)
    x = get_signal(filename, mems)
    f, t, Sxx = signal.spectrogram(x, fs, nperseg=2048)
    plt.pcolormesh(t, f, Sxx,shading='gouraud')
    return t, f, Sxx
    

def spectro(filename,mems):
    """
    Function spectro
    Crée un spectrogramme avec la fonction specgram
    à partir d'un fichier .h5 spécifié et son numéro de
    micro voulu
    
    in : 
    filename : (str) nom du fichier à récupérer
    mems : (int) numéro du micro voulu
    
    out : 
    t : (np.array(float)) axe des abscisses en secondes
    f : (np.array(float)) axe des ordonnées en Hz
    Sxx : (np.array((float, float))) matrice spectrogramme
    """
    fs = int(5e4)
    x = get_signal(filename, mems)
    Pxx, freqs, bins, im = plt.specgram(x, NFFT=2048, Fs=fs, noverlap=900)
