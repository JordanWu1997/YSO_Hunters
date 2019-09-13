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

#==========================================================
# Useful Functions
#==========================================================
def merge_repeated(catalog, outfile='out.tbl', store=False):
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
            SKYC.append(SkyCoord(str(float((REPT[j].split(','))[6])), str(float((REPT[j].split(','))[7])), unit = 'deg', frame = 'fk5'))

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
        survey_list.append(merge_repeated(data))

# Check merge sucess or not
for i, survey in enumerate(survey_list):
    if len(survey) != len(survey_list[0]):
        print('%ith Survey Merge failed ...' % i)

#=============================================
# Merge UKIDSS Surveys
#=============================================
mag_id = [10, 12, 14]
err_id = [11, 13, 15]

merge_output = []
for i in range(len(survey_list[0])):

    # Take first input survey as reference
    source0 = survey_list[0][i].split(',')
    ra0  = float(source0[6])
    dec0 = float(source0[7])

    # If no detection in first input survey, check others
    if ra0 == 0.0 or dec0 == 0.0:
        for j in range(1, len(survey_list)):
            source = survey_list[j][i].split(',')
            ra  = float(source[6])
            dec = float(source[7])

            # If there's detection in others, substitute it for first survey
            if ra != 0.0 and dec != 0.0:
                source0[6], source0[7] = ra, dec
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
