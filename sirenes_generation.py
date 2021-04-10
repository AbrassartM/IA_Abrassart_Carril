import numpy as np
import pylab as plt
import time as time
from scipy import signal
import h5py as h5
import os.path as osp

frequence_sirene ={}
frequence_sirene["fondamentale"]=435
frequence_sirene["police"]=580
frequence_sirene["pompier"]=488
frequence_sirene["samu"]=651
frequence_sirene["gendarmerie"]=732

Fs = int(5e4)

def sirene(type_sirene="fondamentale",duree=5, Fs=50000, nb_harmoniques=10):
    """function sirene
        Genère un signal temporel de sirene

        in:
        type_sirene : (string) nom de la sirène
        duree : (float) duree en seconde du signal de sortie
        Fs : (int) fréquence d'échantillonnage
        nb_harmoniques : nombres d'harmoniques émis

        out:
        F : (np.array(float)) signal temporel de sirene
    """
    f1 = frequence_sirene["fondamentale"]
    f2 = frequence_sirene[type_sirene]
    
    t = np.arange(0, duree, 1/Fs)
    phi = 2*np.pi * np.random.uniform(0,1)
    print(phi)
    F1 = 0
    F2 = 0
    
    for i in range(1,nb_harmoniques+1): # A modifier si besoin 
        s1 = np.sin(2 * np.pi * f1 * i * t+ phi)
        F1 = F1 + s1
        s2 = np.sin(2 * np.pi * f2 * i * t+ phi)
        F2 = F2 + s2
        
    Ns = 0
    Ng = 2.5e4

    for i in range(duree+1):
        for j in range(int(Ng)):
            F1[j+int(Ns)] = 0
        Ns =i* Ng*2
    Ns = Ng
    for i in range(duree):
        for j in range(int(Ng)):
            F2[j+int(Ns)] = 0
        Ns = Ns + Ng*2

    F = F1 +F2
    return F

def spectrogramme(sig,representation='dB'):
    f, t, Sxx = signal.spectrogram(sig, Fs, nperseg=2048)
    if representation=='dB':
        plt.pcolormesh(t, f, 10*np.log10(Sxx),shading='gouraud')
    else:
        plt.pcolormesh(t, f, Sxx,shading='gouraud')
    return t, f, Sxx

def bruit(signal, SNR_dB):
    """
        function bruit
        Ajoute un bruit sur un signal donné

        in:
        signal : (np.array((Nt,)) tableau contenant le signal
        SNR_dB : (float) Signal Noise Ration en dB

        out : 
        signal_bruite (np.array((Nt,))) signal bruite
    """
    
    # Calculate signal power and convert to dB 
    puissance_signal = np.mean(signal**2)
    puissance_signal_dB = 10*np.log10(puissance_signal)
    # print(puissance_signal_dB )
    # SNR_dB = puissance_signal_dB - puissance_signal_bruite_dB
    puissance_signal_bruite_dB = puissance_signal_dB - SNR_dB
    puissance_signal_bruite = 10**(puissance_signal_bruite_dB/10)
    amplitude_signal_bruite = np.sqrt(2*puissance_signal_bruite)
    bruit = amplitude_signal_bruite * np.random.uniform(-1, 1, size=len(signal))
    #print(amplitude_signal_bruite )
    signal_bruite = signal + bruit

    return signal_bruite

if __name__ == '__main__':
    # Cette partie du code n'est appelée que si sirenes_generation.py est executé (pas si il est utilisé comme un module)
    #type_sirene = "police"
    liste_sirenes=["police", "pompier", "samu", "gendarmerie"]
    nb_signaux = 1
    for type_sirene in liste_sirenes:
        for i in range(nb_signaux):
            sig = sirene(type_sirene=type_sirene,duree=20,nb_harmoniques=5)
            signal_bruit = bruit(sig, 6)
            filen = type_sirene + "_signal_" + str(i) + ".h5"
            filename = osp.join("../data", filen)
            print(filename)
            with h5.File(filename,'w') as h5file:
                h5file.create_dataset(name="signal", data=signal_bruit)
        plt.figure()
        t, f, Sxx = spectrogramme(signal_bruit)
        plt.title(type_sirene)
        plt.xlabel('Temps [s]'), plt.ylabel('Fréquence [Hz]')
        plt.axis((t[0],t[-1],0,10000))
    #plt.figure()
    #plt.plot(aud_pol[0:3000])
    #plt.plot(bruit(aud_pol[0:3000],20))
    plt.show()
    
    
def doppler(signal, duree, vit, SNR_dB) :
    """
        function doppler
        Ajoute un effet doppler sur un signal donné

        in:
        signal : (np.array((Nt,)) tableau contenant le signal
        duree : (float)  duree du signal généré
        vit : (float) vitesse à laquelle roule le véhicule d'urgence en km/h
        SNR_dB : (float) intensité du bruit blanc

        out : 
        R (np.array((Nt,))) signal bruite+doppler
    """
    sig = bruit(signal, SNR_dB)
    Fs = 5e4
    c = vit
    dur = duree 
    samples = int(Fs*dur)
    t = np.arange(0, dur, 1/Fs)
    
    x = t * c
    x -= x.max()/2.0 
    y = np.zeros(samples)
    z = 100.0 * np.ones(samples)
    
    position_source = np.vstack((x,y,z)).T
    position_receiver = np.zeros(3)
    distance = np.linalg.norm((position_source - position_receiver), axis=-1)
    c0 = 340
    delay = distance / c0
    
    # Interpolation
    k_r = np.arange(0, len(sig), 1)
    k = k_r - delay * Fs
    kf = np.floor(k).astype(int)
    R = ( (1.0-k+kf) * sig[kf] + (k-kf) * sig[kf+1] ) * (kf >= 0)
    return R