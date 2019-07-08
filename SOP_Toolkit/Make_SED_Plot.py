#!/usr/bin/ipython

import os
import random
import math as mth
import numpy as np
from sys import argv, exit
import matplotlib.pyplot as plt

if len(argv) != 4:
    exit('Example: python [program] [input catalog] [piece-size] [Normalize]\n\
         piece-size: SED # in ALL_SED_PLOT\n\
         normalize: True/False (default: False')
else:
    print('Start ploting ...')

# Bands names
band = ['J', 'H', 'Ks', 'IR1', 'IR2', 'IR3', 'IR4', 'MP1', 'MP2']
# For J, H, Ks, flux must be calculated from magnitude
JHK_f0 = [1594000.0, 1024000.0, 666700.0]
# Wavelength unit: micrometer
wavelength = [1.235, 1.662, 2.159, 3.6, 4.5, 5.8, 8.0, 24.0, 70.0]
# For J, H, Ks, indice are mag indice, others are flux indice
col_index = [35, 56, 77, 96, 117, 138, 159, 180, 201]
# For IR1-MP1
flux_qua = ['no', 'no', 'no', 100, 121, 142, 163, 184, 205]

if os.path.isdir('SED_PLOT'):
    os.system('rm -fr SED_PLOT')
    os.system('mkdir SED_PLOT')
else:
    os.system('mkdir SED_PLOT')
if os.path.isdir('ALL_SED_PLOT'):
    os.system('rm -fr ALL_SED_PLOT')
    os.system('mkdir ALL_SED_PLOT')
else:
    os.system('mkdir ALL_SED_PLOT')

cat = open(str(argv[1]), 'r')
data = cat.readlines()
cat.close()

os.chdir('SED_PLOT')
print('\nMake SED PLOT individually ...')
Norm = str(argv[3])
for i in range(len(data)):
    print(str(i+1) + '/' + str(len(data)))
    flux_list = []
    qua_list = ''
    row = data[i].split()
    for j in range(len(JHK_f0)):
        if float(row[col_index[j]]) > 0.0:
            flux = JHK_f0[j] * 10**(float(row[col_index[j]])/(-2.5))
        else:
            flux = 0.0
        flux_list.append(flux)
    for k in range(len(JHK_f0), len(col_index)):
        if float(row[col_index[k]]) > 0.0:
            flux = float(row[col_index[k]])
        else:
            flux = 0.0
        flux_list.append(flux)
        qua_list += str(row[flux_qua[k]])
    x, y = [], []
    plt.figure()
    for l in range(len(wavelength)):
        if flux_list[l] != 0.0:
            x.append(wavelength[l])
            if Norm == 'True':
                y.append(flux_list[l]/max(flux_list))
            else:
                y.append(wavelength[l] * flux_list[l])
        plt.axvline(wavelength[l], color = 'k', linestyle = '--')
    plt.loglog(x, y, 'ro-')
    plt.yscale('log')
    plt.xscale('log')
    plt.xlabel('wavelength (um)')
    if Norm == 'True':
        plt.ylabel('Normalized wavelength * flux')
    else:
        plt.ylabel('wavelength * flux (um * mJansky)')
    plt.grid(True)
    plt.savefig(str(i+1) + '-' + qua_list + '-SED.png')

os.chdir('../ALL_SED_PLOT')
piece = int(argv[2])
counter = len(data)

color_list = []
if piece <= 10:
    for i in range(piece):
        color_list.append('C'+str(i))
else:
    for i in range(piece):
        color_list.append('C'+str(i))
    for j in range(10, piece):
        color_list.append((round(random.random(), 3), round(random.random(), 3), round(random.random(), 3)))

for h in range((len(data)//piece)+1):
    plt.figure(figsize=(18,9))
    print('\nMake all SED PLOT ...')
    print(str(h+1) + '/' + str((len(data) // piece)+1))
    if counter > piece:
        for i in range(piece * h, piece * (h+1)):
            flux_list = []
            row = data[i].split()
            for j in range(len(JHK_f0)):
                if float(row[col_index[j]]) > 0.0:
                    flux = JHK_f0[j] * 10**(float(row[col_index[j]])/(-2.5))
                else:
                    flux = 0.0
                flux_list.append(flux)
            for k in range(len(JHK_f0), len(col_index)):
                if float(row[col_index[k]]) > 0.0:
                    flux = float(row[col_index[k]])
                else:
                    flux = 0.0
                flux_list.append(flux)
            x, y = [], []
            for l in range(len(wavelength)):
                if flux_list[l] != 0.0:
                    x.append(wavelength[l])
                    if Norm == 'True':
                        y.append(flux_list[l]/max(flux_list))
                    else:
                        y.append(wavelength[l] * flux_list[l])
                plt.axvline(wavelength[l], color = 'k', linestyle = '--')
            plt.loglog(x, y, c=color_list[(i%piece)], ls='--', marker='o', label=str(i+1))
            plt.xlabel('wavelength (um)')
            if Norm == 'True':
                plt.ylabel('Normalized wavelength * flux')
            else:
                plt.ylabel('wavelength * flux (um * mJansky)')
            plt.yscale('log')
            plt.xscale('log')
            plt.legend()
            plt.grid(True)
            plt.savefig('ALL-SED-' + str(h+1) + '.png')
    else:
        for i in range(piece*h, len(data)):
            flux_list = []
            row = data[i].split()
            for j in range(len(JHK_f0)):
                if float(row[col_index[j]]) > 0.0:
                    flux = JHK_f0[j] * 10**(float(row[col_index[j]])/(-2.5))
                else:
                    flux = 0.0
                flux_list.append(flux)
            for k in range(len(JHK_f0), len(col_index)):
                if float(row[col_index[k]]) > 0.0:
                    flux = float(row[col_index[k]])
                else:
                    flux = 0.0
                flux_list.append(flux)
            x, y = [], []
            for l in range(len(wavelength)):
                if flux_list[l] != 0.0:
                    x.append(wavelength[l])
                    if Norm == 'True':
                        y.append(flux_list[l]/max(flux_list))
                    else:
                        y.append(wavelength[l] * flux_list[l])
                plt.axvline(wavelength[l], color = 'k', linestyle = '--')
            plt.loglog(x, y, c=color_list[i%piece], ls='--', marker='o', label=str(i+1))
            plt.xlabel('wavelength (um)')
            if Norm == 'True':
                plt.ylabel('Normalized wavelength * flux')
            else:
                plt.ylabel('wavelength * flux (um * mJansky)')
            plt.yscale('log')
            plt.xscale('log')
            plt.legend()
            plt.grid(True)
            plt.savefig('ALL-SED-' + str(h+1) + '.png')
    counter -= piece
