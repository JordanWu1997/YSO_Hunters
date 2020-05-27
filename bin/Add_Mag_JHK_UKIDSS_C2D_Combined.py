#!/usr/bin/python
'''-------------------------------------------------------------------------------------
This program is to write :
    (1) new UKIDSS J,H,K mag and error
    (2) old SWIRE IR1,IR2,IR3,IR4,MP1 mag and error to an old SWIRE catalog (for ELAIS N1)

Example: [Program] [C2D] [UKIDSS] [Header length] [Output filename] [Option]

Input Variables:
    [Option]: 2MASSBR <= keep 2MASS Bright Sources (Jmag>11.5)
    [Header length]: 13 for DR11PLUS
    **Note**: This Program Replace [C2D] J,H,K with [UKIDSS]

**NOTE**
    Since UKIDSS catalog has a saturate issue, we use new UKIDSS data with condition:
       (1) Replace UKIDSS data ONLY with J band magnitude larger than 11.5 mag
       (2) For UKIDSS data with J band magnitude smaller than 11.5 mag, reject to replace
           with UKIDSS data. However, 2MASS data still have to do calibration to UKIDSS format

    1. Empty columns on SWIRE format catalog for storing UKIDSS magnitude and error
       (1) magnitude: J[35], H[56], K[77]
       (2) mag_err: J[36], H[57], K[78]

    2. Empty columns on SWIRE format catalog for storing SWIRE mag and error
       (1) magnitude: IR1[102], IR2[123], IR3[144], IR4[165], MP1[186]
       (2) mag_err: IR1[103], IR2[124], IR3[145], IR4[166], MP1[187]

    3. If a band is undetected, the magnitude and error will be assigned as '0.0'

---------------------------------------------------------------------------------------
latest update : 2020/05/26 Jordan Wu'''

# Import Modules
#==========================================================
from __future__ import print_function
from Hsieh_Functions import *
from Useful_Functions import *
from sys import argv, exit
from astropy.coordinates import SkyCoord
import time

# Index of parameters on UKIDSS catalog
#=======================================
TABLE = 'DR11PLUS'
# DR11PLUS: Used For Molecular Clouds
# DR10PLUS: Used For Galaxies

# Functions
#==========================================================
def merge_repeated(catalog, outfile='out.tbl', store=False):
    '''
    This function is to merge sources with repeated ID in UKIDSS survey
    '''
    # Find repeated sources
    Repeat_dict = {}
    print('Start finding repeated sources ...\n')
    for i in range(len(catalog)):
        index = int(catalog[i].split()[0].strip(',')) - 1
        Repeat_dict.update({index: ''})
        Repeat_dict[index] += catalog[i] + ';'
        if i > 1000 and i % 1000 == 0:
            print('%.6f' % (100*float(i)/float(len(catalog))) + '%')
    print('Complete finding repeated sources ...\n')

    # Start merging
    m_start = time.time()
    no_rpt_catalog = []
    print('Start comparing repeated sources distances to target\n')
    for i in range(len(Repeat_dict)):
        if i>1000 and i%1000==0:
            print('%.6f' % (100*float(i)/float(len(Repeat_dict))) + '%')
        REPT  = Repeat_dict[i].split(';')[:-1]
        ra0   = "{:.7f}".format(float((REPT[0].split(','))[Ref_Coor_ID[0]]))
        dec0  = "{:.7f}".format(float((REPT[0].split(','))[Ref_Coor_ID[1]]))
        SKYC0 = SkyCoord(ra0, dec0, unit="deg", frame='fk5')
        SKYC, SEP = [], []
        for j in range(len(REPT)):
            ra  = "{:.7f}".format(float((REPT[0].split(','))[UCoor_ID[0]]))
            dec = "{:.7f}".format(float((REPT[0].split(','))[UCoor_ID[1]]))
            SKYC.append(SkyCoord(ra, dec, unit = 'deg', frame = 'fk5'))
        for k in range(len(SKYC)):
            SEP.append(SKYC0.separation(SKYC[k]).value)
        ind = SEP.index(max(SEP))
        no_rpt_catalog.append(REPT[ind])
    m_end   = time.time()
    print('\nComplete comparing distances between repeated sources ...\
             Dealing with repeated sources in catalog took %.6f secs ...\n'.format(m_end - m_start))

    # Save corrected catalog or not
    if store:
        print('Saving merged catalog ...\n')
        with open(outfile, 'w') as output:
            for i, row in enumerate(no_rpt_catalog):
                if i > 1000 and i % 1000 == 0:
                    output.write(str(row))
                    print('%.6f' % (100*float(i)/float(len(no_rpt_catalog))) + '%')
    return no_rpt_catalog

#=====================================================================
# Load input catalog and apply input file check for repeating sources
#=====================================================================
if __name__ == '__main__':
    t_start = time.time()

    # Check inputs
    if len(argv) != 6:
        exit('\n\tWrong Input Argument!\
            \n\tExample: [Program] [C2D] [UKIDSS] [Header length] [Output filename] [Option]\
            \n\t[Option]: 2MASSBR <= keep 2MASS Bright Sources (Jmag>11.5)\
            \n\t**Note**: This Program Replace [C2D] J,H,K with [UKIDSS]\n')

    # Input variables
    two_mass_name = str(argv[1])
    ukidss_name   = str(argv[2])
    header_length = int(argv[3])
    out_name      = str(argv[4])
    option        = str(argv[5])

    # Print out info
    flux_J_ID, flux_H_ID, flux_K_ID          = tuple(flux_ID_2Mass)
    mag_J_ID, mag_H_ID, mag_K_ID             = tuple(mag_ID_2Mass)
    mag_err_J_ID, mag_err_H_ID, mag_err_K_ID = tuple(mag_err_ID_2Mass)

    Ref_Coor_ID = [7, 8] # Ra, Dec Input to search
    UCoor_ID    = [1, 2] # Ra, Dec on UKIDSS catalog
    if TABLE == 'DR10PLUS':
        UMag_ID  = [10, 12, 14] # J, H, K mag indice
        UErr_ID  = [11, 13, 15] # J, H, K error indice
    elif TABLE == 'DR11PLUS':
        # ID For MagType: AperMag3
        UMag_ID = [55, 80, 105] # J, H, K mag indice
        UErr_ID = [56, 81, 106] # J, H, K error indice
    print('\n\tTABLE   : {}\
           \n\tBAND    : {}\
           \n\tUCoor   : {}\
           \n\tRefCoor : {}\
           \n\tMAG_ID  : {}\
           \n\tERR_ID  : {}\n'.format(TABLE, 'JHK', str(UCoor_ID), str(Ref_Coor_ID), str(UMag_ID), str(UErr_ID)))

    # Load catalogs
    with open(ukidss_name, 'r') as data:
        ukidss_cat_origin = data.readlines()[header_length:]
    with open(two_mass_name, 'r') as data:
        two_mass_cat = data.readlines()
    # Check if merge is needed
    if len(two_mass_cat) < len(ukidss_cat_origin):
        print('Repeated source ID found ...\n')
        ukidss_cat = merge_repeated(ukidss_cat_origin)
    else:
        ukidss_cat = ukidss_cat_origin

    # Replace 2MASS Observation with UKIDSS Survey
    num1, num2 = 0, 0
    out_catalog = []
    for i in range(len(ukidss_cat)):
        # Percentage Indicator
        drawProgressBar(float(i+1)/len(ukidss_cat))
        # Loading Sources
        index = int(ukidss_cat[i].split()[0].strip(',')) - 1
        row_s = two_mass_cat[index].split()
        row_u = ukidss_cat[i].split(',')
        # Write SWIRE Format IR1~MP1 magnitude and error
        mag_list = mJy_to_mag_ONLY_Spitzer(row_s)
        err_list = flux_error_to_mag_ONLY_Spitzer(row_s)
        for j in range(len(mag_list)):
            row_s[mag_ID_Spitzer[j]]     = str(mag_list[j])
            row_s[mag_err_ID_Spitzer[j]] = str(err_list[j])
        # Write UKIDSS JHK magnitude and error
        mag_uJ, mag_uH, mag_uK = row_u[UMag_ID[0]], row_u[UMag_ID[1]], row_u[UMag_ID[2]]
        err_uJ, err_uH, err_uK = row_u[UErr_ID[0]], row_u[UErr_ID[1]], row_u[UErr_ID[2]].strip('\n')

        # If No Detection => Transform from 2MASS to UKIDSS
        if float(row_u[UCoor_ID[0]]) == 0.0 or float(row_u[UCoor_ID[1]]) == 0.0:
            num1 += 1
            mag_J, mag_H, mag_K = JHK_flux_to_mag(row_s[flux_J_ID], row_s[flux_H_ID], row_s[flux_K_ID])
            row_s[mag_J_ID], row_s[mag_H_ID], row_s[mag_K_ID] = str(mag_J), str(mag_H), str(mag_K)
            row_s[mag_err_J_ID], row_s[mag_err_H_ID], row_s[mag_err_K_ID] = '0.0', '0.0', '0.0'
        else:
            row_s[mag_J_ID], row_s[mag_H_ID], row_s[mag_K_ID] = mag_uJ, mag_uH, mag_uK
            row_s[mag_err_J_ID], row_s[mag_err_H_ID], row_s[mag_err_K_ID] = err_uJ, err_uH, err_uK

        # Pick Up Bright Sources In 2MASS Observation
        if option == '2MASSBR':
            if float(mag_uJ) < 11.5:
                num2 += 1
                mag_J, mag_H, mag_K = JHK_flux_to_mag(row_s[flux_J_ID], row_s[flux_H_ID], row_s[flux_K_ID])
                row_s[mag_J_ID], row_s[mag_H_ID], row_s[mag_K_ID] = str(mag_J), str(mag_H), str(mag_K)
                row_s[mag_err_J_ID], row_s[mag_err_H_ID], row_s[mag_err_K_ID] = '0.0', '0.0', '0.0'
        # Write New Output Catalog
        out_catalog.append('\t'.join(row_s) + '\n')

    # Write Output
    with open(out_name, 'w') as out:
        for row in out_catalog:
            out.write(row)

    # Print out results
    t_end   = time.time()
    print('\nWhole {} process took {:.3f} secs\
           \nNon-Detection In UKIDSS survey: {:d}\
           \nBright Source In 2MASS survey:  {:d}\
           \nAll Source In {}: {:d}\n'.format(str(argv[0]), t_end - t_start, num1, num2, two_mass_name, len(out_catalog)))
