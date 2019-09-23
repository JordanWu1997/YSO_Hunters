#!/usr/bin/ipython
'''
---------------------------------------------------------------------------------------

---------------------------------------------------------------------------------------
latest update : 2019/09/13 Jordan Wu'''

from sys import argv, exit
from astropy.coordinates import SkyCoord
import numpy as np
import time

if len(argv) <= 2:
    exit('\n\tWrong Input Argument!\
        \n\tExample: [Program] [Output filename] [Catalogs to merge ...]\
        \n\t[Catalogs to merge]: input catalogs respectively\n')

#=======================================
# Index of parameters on UKIDSS catalog
#=======================================
Coor_ID = [7, 8]       # Ra, Dec

# IN DR10PLUS
# Mag_ID  = [10, 12, 14] # J, H, K
# Err_ID  = [11, 13, 15] # J, H, K

# IN DR11PLUS
#MagType: AperMag3
#J_mag ID: 55
#H_mag ID: 80
#K_mag ID: 105
#J_err ID: 56
#H_err ID: 81
#K_err ID: 106
Mag_ID = [55, 80, 105]
Err_ID = [56, 81, 106]

#==========================================================
# Useful Functions
#==========================================================
def merge_repeated(catalog, outfile='out.tbl', store=False, ra_id=Coor_ID[0], dec_id=Coor_ID[1]):
    '''
    This function is to merge sources with repeated ID in UKIDSS survey
    '''
    Repeat_dict = {}
    print('Start finding repeated sources ...\n')
    for i in range(len(catalog)):
        index = int(catalog[i].split()[0].strip(',')) - 1
        Repeat_dict.update({index: ''})
        Repeat_dict[index] += catalog[i] + ';'
        if i>1000 and i%1000==0:
            print('%.6f' % (100*float(i)/float(len(catalog))) + '%')
    print('Complete finding repeated sources ...\n')

    no_rpt_catalog = []
    print('Start comparing repeated sources distances to target\n')
    for i in range(len(Repeat_dict)):
        if i>1000 and i%1000==0:
            print('%.6f' % (100*float(i)/float(len(Repeat_dict))) + '%')

        REPT = Repeat_dict[i].split(';')[:-1]
        SKYC = []
        for j in range(len(REPT)):
            ra0 = str(float((REPT[j].split(','))[1]))
            dec0 = str(float((REPT[j].split(','))[2]))
            SKYC0 = SkyCoord(ra0, dec0, unit="deg", frame='fk5')
            SKYC.append(SkyCoord(str(float((REPT[j].split(','))[ra_id])), str(float((REPT[j].split(','))[dec_id])), unit = 'deg', frame = 'fk5'))

        SEP = []
        for k in range(len(SKYC)):
            SEP.append(SKYC0.separation(SKYC[k]).value)
        ind = SEP.index(max(SEP))
        no_rpt_catalog.append(REPT[ind])

    t_end = time.time()
    print('Complete comparing distances between repeated sources ...\n')
    print('Dealing with repeated sources in catalog took %.6f secs ...\n' % (t_end - t_start))

    if store == True:
        # Save corrected catalog
        print('Saving merged catalog ...\n')
        with open(outfile, 'w') as output:
            for i, row in enumerate(no_rpt_catalog):
                if i>1000 and i%1000==0:
                    print('%.6f' % (100*float(i)/float(len(no_rpt_catalog))) + '%')
                output.write(str(row))
    return no_rpt_catalog


#=============================================
# Merge Repeated Source Respectivily
#=============================================
input_list = [str(inp) for inp in argv[2:]]
survey_list = []
for inp in input_list:
    with open(inp, 'r') as data:
        catalog = data.readlines()[13:]
        survey_list.append(merge_repeated(catalog))

# Check merge sucess or not
for i, survey in enumerate(survey_list):
    if len(survey) != len(survey_list[0]):
        print('%ith Survey Merge failed ...' % i)

#=============================================
# Merge UKIDSS Surveys
#=============================================
merge_output = []
for i in range(len(survey_list[0])):

    # Take first input survey as reference
    source0 = survey_list[0][i].split(',')
    ra0  = float(source0[7])
    dec0 = float(source0[8])

    # If no detection in first input survey, check others
    if ra0 == 0.0 or dec0 == 0.0:
        for j in range(1, len(survey_list)):
            source = survey_list[j][i].split(',')
            ra  = float(source[7])
            dec = float(source[8])

            # If there's detection in others, substitute it for first survey
            if ra != 0.0 and dec != 0.0:
                source0[7], source0[8] = ra, dec
                for mag in mag_id:
                    source0[mag] = source[mag]
                for err in err_id:
                    source0[err] = source[err]

    # Save merged source
    source_m = ','.join(source0)
    merge_output.append(source_m)

#=============================================
# Save UKIDSS survey-merged file
#=============================================
with open(str(argv[1]), 'w') as out:
    for output in merge_output:
        out.write(output)
