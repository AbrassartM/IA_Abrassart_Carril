#!/usr/bin/env python
# coding: utf-8

# # Fonctions BDD Signaux artificiels

# In[1]:


import csv
import pylab as plt
import numpy as np
from scipy import signal
import scipy.io.wavfile as wav


# In[21]:


def BDD_type(typ):
    fname = "BDD_Signaux_Artificiels.csv"
    file = open(fname, "r")
 
    reader = csv.reader(file)
    BDD_utile = []
    for row in reader :
        if typ in row[1] :
            BDD_utile.append(row[0])
    file.close()
    return BDD_utile


# In[24]:


def BDD_sirene(sirene):
    fname = "BDD_Signaux_Artificiels.csv"
    file = open(fname, "r")
 
    reader = csv.reader(file)
    BDD_utile = []
    
    for row in reader :
        for i in row :
            if sirene in i :
                BDD_utile.append(i)
                
    file.close()
    return BDD_utile


# In[26]:


def BDD(sirene, typ):
    fname = "BDD_Signaux_Artificiels.csv"
    file = open(fname, "r")
 
    reader = csv.reader(file)
    BDD_utile = []
    
    for row in reader :
        if typ in row[1] :
            for i in row :
                if sirene in i :
                    BDD_utile.append(row[0])
    file.close()
    return BDD_utile


def return_image(liste, path):
    d = 0
    L = np.zeros((len(liste), 41, 27))
    for j in range(0,len(liste)):
        sig = liste[j]
        sig = sig[0:18]+'.wav'

        fichier = path+'/'+sig
        Fe_vect, x = wav.read(fichier)
        
        fs = int(5e4)

        x_2 = np.reshape(x,(len(x)//fs,fs))
        for i in range(1,len(x_2[:,0])+1):
            sign = liste[j]
            if i == int(sign[18:20]):
                f, t, Sxx = signal.spectrogram(x_2[i-1,:], fs, nperseg=2048)
                Sxx_2 = Sxx[0 : len(Sxx[:,0])//5 , :]
                Sxx_3 = np.zeros((len(Sxx_2[:,0])//5, len(Sxx_2[0,:])))
                for h in range(0,len(Sxx_3[:,0])):
                    Sxx_3[h,:] = np.mean(Sxx_2[5*h : 5*(h+1) , :], axis = 0)
                L[d,:] = Sxx_3 
                d = d+1
    return L
          