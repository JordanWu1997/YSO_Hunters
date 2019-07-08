#! usr/bin/python
from numpy import *
from os import system, chdir
'----------------------------------------------------------------------------------------------------'

'----------------------------------------------------------------------------------------------------'
print("Load...")
Gal_pos=load("../GPV_bin0.4/Gal_Position_vectors.npy")
six_beam=load("../ND_Beam_sigma2/6d_beam_sigma2.npy")
fi_beam=load("../ND_Beam_sigma2/5d_beam_sigma2.npy")
fo_beam=load("../ND_Beam_sigma2/4d_beam_sigma2.npy")
th_beam=load("../ND_Beam_sigma2/3d_beam_sigma2.npy")
shape=load("../GPV_bin0.4/Shape.npy")
shape=list(shape)
'----------------------------------------------------------------------------------------------------'
print("Start Calculation")
'----------------------------------------------------------------------------------------------------'
d66={}
d65={}
d64={}
d63={}
d55={}
d54={}
d53={}
d44={}
d43={}
d33={}
'----------------------------------------------------------------------------------------------------'
for li in range(len(Gal_pos)):
    gal=list(Gal_pos[li])
    if li%100==0:
        print('Now : ' + str(float(li)/len(Gal_pos) * 100) + '%')
# 6bands sources
    if gal.count("Lack")==0 and gal.count("Faint")==0:
# aply to six bands
        new_gal=list(gal)
        i=int(new_gal[0]);j=int(new_gal[1]);k=int(new_gal[2]);l=int(new_gal[3]);m=int(new_gal[4]);n=int(new_gal[5])
        for v in range(len(six_beam)):
            vec=list(six_beam[v])
            vec[0]=int(vec[0]);vec[1]=int(vec[1]);vec[2]=int(vec[2]);vec[3]=int(vec[3]);vec[4]=int(vec[4]);vec[5]=int(vec[5])
            if 0<=i+vec[0]<shape[0] and 0<=j+vec[1]<shape[1] and 0<=k+vec[2]<shape[2] and 0<=l+vec[3]<shape[3] and 0<=m+vec[4]<shape[4] and 0<=n+vec[5]<shape[5]:
                #fid_smooth_array[i+vec[0]][j+vec[1]][k+vec[2]][l+vec[3]][m+vec[4]][n+vec[5]] += vec[6]*int(new_gal[6])
                try:
                    d66[str((i+vec[0], j+vec[1], k+vec[2], l+vec[3], m+vec[4], n+vec[5])).strip("( )")] +=vec[6]*int(new_gal[6])
                except KeyError :
                    d66.update({str((i+vec[0], j+vec[1], k+vec[2], l+vec[3], m+vec[4], n+vec[5])).strip("( )") : vec[6]*int(new_gal[6])})

# aply to five bands    
        for dia in range(6):
            new_gal=list(gal)
            del new_gal[dia]
            new_shape=list(shape)
            del new_shape[dia]
            i=int(new_gal[0]);j=int(new_gal[1]);k=int(new_gal[2]);l=int(new_gal[3]);m=int(new_gal[4])
            for v in range(len(fi_beam)):
                vec=list(fi_beam[v])
                vec[0]=int(vec[0]);vec[1]=int(vec[1]);vec[2]=int(vec[2]);vec[3]=int(vec[3]);vec[4]=int(vec[4])
                if 0<=i+vec[0]<new_shape[0] and 0<=j+vec[1]<new_shape[1] and 0<=k+vec[2]<new_shape[2] and 0<=l+vec[3]<new_shape[3] and 0<=m+vec[4]<new_shape[4]:
                    #Lack_all[dia][dia][i+vec[0]][j+vec[1]][k+vec[2]][l+vec[3]] += vec[4]*int(new_gal[4])
                    key_l = [i+vec[0], j+vec[1], k+vec[2], l+vec[3], m+vec[4]]
                    key_n = (str(key_l[0:dia] + ['Lack'] + key_l[dia:])).strip("[ ]")
                    try:
                        d65[key_n] +=vec[5]*int(new_gal[5])
                    except KeyError :
                        d65.update({key_n : vec[5]*int(new_gal[5])})

# aply to four bands
        for A in range(6):
            for B in range(A):
                new_gal=list(gal)
                del new_gal[B], new_gal[A-1]
                new_shape=list(shape)
                del new_shape[B],new_shape[A-1]
                i=int(new_gal[0]);j=int(new_gal[1]);k=int(new_gal[2]);l=int(new_gal[3])
                for v in range(len(fo_beam)):
                    vec=list(fo_beam[v])
                    vec[0]=int(vec[0]);vec[1]=int(vec[1]);vec[2]=int(vec[2]);vec[3]=int(vec[3])
                    if 0<=i+vec[0]<new_shape[0] and 0<=j+vec[1]<new_shape[1] and 0<=k+vec[2]<new_shape[2] and 0<=l+vec[3]<new_shape[3]:
                        #Lack_all[B][A][i+vec[0]][j+vec[1]][k+vec[2]] += vec[3]*int(new_gal[3])
                        key_l = [i+vec[0], j+vec[1], k+vec[2], l+vec[3]]
                        key_n = (str(key_l[0:B] + ['Lack'] + key_l[B:A] + ['Lack'] + key_l[A:])).strip("[ ]")
                        try:
                            d64[key_n] +=vec[4]*int(new_gal[4])
                        except KeyError :
                            d64.update({key_n : vec[4]*int(new_gal[4])})


# aply to three bands
        for A in range(6):
            for B in range(A):
                for C in range(B):
                    new_gal=list(gal)
                    del new_gal[C], new_gal[B-1], new_gal[A-2]
                    new_shape=list(shape)
                    del new_shape[C], new_shape[B-1], new_shape[A-2]
                    i=int(new_gal[0]);j=int(new_gal[1]);k=int(new_gal[2])
                    for v in range(len(th_beam)):
                        vec=list(th_beam[v])
                        vec[0]=int(vec[0]);vec[1]=int(vec[1]);vec[2]=int(vec[2])
                        if 0<=i+vec[0]<new_shape[0] and 0<=j+vec[1]<new_shape[1] and 0<k+vec[2]<new_shape[2]:
                            key_l = [i+vec[0], j+vec[1], k+vec[2]]
                            key_n = (str(key_l[0:C] + ['Lack'] + key_l[C:B] + ['Lack'] + key_l[B:A] + ['Lack'] + key_l[A:])).strip("[ ]")
                            try:
                                d63[key_n] += vec[3]*int(new_gal[3])
                            except KeyError :
                                d63.update({key_n : vec[3]*int(new_gal[3])})



# 5bands sources
    elif gal.count("Lack")==1 and gal.count("Faint")==0:
        new_gal=list(gal)
        L1=new_gal.index("Lack")
# aply to five bands
        del new_gal[L1]
        new_shape=list(shape)
        del new_shape[L1]
        i=int(new_gal[0]);j=int(new_gal[1]);k=int(new_gal[2]);l=int(new_gal[3]);m=int(new_gal[4])
        for v in range(len(fi_beam)):
            vec=list(fi_beam[v])
            vec[0]=int(vec[0]);vec[1]=int(vec[1]);vec[2]=int(vec[2]);vec[3]=int(vec[3]);vec[4]=int(vec[4])
            if 0<=i+vec[0]<new_shape[0] and 0<=j+vec[1]<new_shape[1] and 0<=k+vec[2]<new_shape[2] and 0<=l+vec[3]<new_shape[3] and 0<=m+vec[4]<new_shape[4]:
                #Lack_all[L1][L1][i+vec[0]][j+vec[1]][k+vec[2]][l+vec[3]] += vec[4]*int(new_gal[4])
                key_l = [i+vec[0], j+vec[1], k+vec[2], l+vec[3], m+vec[4]]
                key_n = (str(key_l[0:L1] + ['Lack'] + key_l[L1:])).strip("[ ]")
                try:
                    d55[key_n] += vec[5]*int(new_gal[5])
                except KeyError :
                    d55.update({key_n : vec[5]*int(new_gal[5])})

# aply to four bands
        for A in range(6):
            for B in range(A):
                if A==L1 or B==L1:
                    new_gal=list(gal)
                    del new_gal[B], new_gal[A-1]
                    new_shape=list(shape)
                    del new_shape[B], new_shape[A-1]
                    i=int(new_gal[0]);j=int(new_gal[1]);k=int(new_gal[2]);l=int(new_gal[3])
                    for v in range(len(fo_beam)):
                        vec=list(fo_beam[v])
                        vec[0]=int(vec[0]);vec[1]=int(vec[1]);vec[2]=int(vec[2]);vec[3]=int(vec[3])
                        if 0<=i+vec[0]<new_shape[0] and 0<=j+vec[1]<new_shape[1] and 0<=k+vec[2]<new_shape[2] and 0<=l+vec[3]<new_shape[3]:
                            key_l = [i+vec[0], j+vec[1], k+vec[2], l+vec[3]]
                            key_n = (str(key_l[0:B] + ['Lack'] + key_l[B:A] + ['Lack'] + key_l[A:])).strip("[ ]")
                            try:
                                d54[key_n] +=vec[4]*int(new_gal[4])
                            except KeyError :
                                d54.update({key_n : vec[4]*int(new_gal[4])})


# aply to three bands
        for A in range(6):
            for B in range(A):
                for C in range(B):
                    if A==L1 or B==L1 or C==L1:
                        new_gal=list(gal)
                        del new_gal[C], new_gal[B-1], new_gal[A-2]
                        new_shape=list(shape)
                        del new_shape[C], new_shape[B-1], new_shape[A-2]
                        i=int(new_gal[0]);j=int(new_gal[1]);k=int(new_gal[2])
                        for v in range(len(th_beam)):
                            vec=list(th_beam[v])
                            vec[0]=int(vec[0]);vec[1]=int(vec[1]);vec[2]=int(vec[2])
                            if 0<=i+vec[0]<new_shape[0] and 0<=j+vec[1]<new_shape[1] and 0<=k+vec[2]<new_shape[2]:
                            #Lack_all[B][A][i+vec[0]][j+vec[1]][k+vec[2]] += vec[3]*int(new_gal[3])
                                key_l = [i+vec[0], j+vec[1], k+vec[2]]
                                key_n = (str(key_l[0:C] + ['Lack'] + key_l[C:B] + ['Lack'] + key_l[B:A] + ['Lack'] + key_l[A:])).strip("[ ]")
                                try:
                                    d53[key_n] += vec[3]*int(new_gal[3])
                                except KeyError :
                                    d53.update({key_n : vec[3]*int(new_gal[3])})

# 4bands source
# aply to four bands
    elif gal.count("Lack")==2 and gal.count("Faint")==0:
	new_gal=list(gal)
	L1=new_gal.index("Lack")
	del new_gal[L1]
	L2=new_gal.index("Lack")
	del new_gal[L2]
	new_shape=list(shape)
	del new_shape[L1],new_shape[L2]
	L2=L2+1
	i=int(new_gal[0]);j=int(new_gal[1]);k=int(new_gal[2]);l=int(new_gal[3])
	for v in range(len(fo_beam)):
	    vec=fo_beam[v]
            vec[0]=int(vec[0]);vec[1]=int(vec[1]);vec[2]=int(vec[2]);vec[3]=int(vec[3])
	    if 0<=i+vec[0]<new_shape[0] and 0<=j+vec[1]<new_shape[1] and 0<=k+vec[2]<new_shape[2] and 0<=l+vec[3]<new_shape[3]:
                #Lack_all[L1][L2][i+vec[0]][j+vec[1]][k+vec[2]] += vec[3]*int(new_gal[3])
                key_l = [i+vec[0], j+vec[1], k+vec[2], l+vec[3]]
                key_n = (str(key_l[0:L1] + ['Lack'] + key_l[L1:L2] + ['Lack'] + key_l[L2:])).strip("[ ]")
                try:
                    d44[key_n] +=vec[4]*int(new_gal[4])
                except KeyError :
                    d44.update({key_n : vec[4]*int(new_gal[4])})

# aply to three bands (new method)
        for A in range(6):
            for B in range(A):
                for C in range(B):
                    if (A==L1 and B==L2) or (A==L1 and C==L2) or (B==L1 and A==L2) or (B==L1 and C==L2) or (C==L1 and A==L2) or (C==L1 and B==L2):
                        new_gal=list(gal)
                        del new_gal[C], new_gal[B-1], new_gal[A-2]
                        new_shape=list(shape)
                        del new_shape[C], new_shape[B-1], new_shape[A-2]
                        i=int(new_gal[0]);j=int(new_gal[1]);k=int(new_gal[2])
                        for v in range(len(th_beam)):
                            vec=list(th_beam[v])
                            vec[0]=int(vec[0]);vec[1]=int(vec[1]);vec[2]=int(vec[2])
                            if 0<=i+vec[0]<new_shape[0] and 0<=j+vec[1]<new_shape[1] and 0<=k+vec[2]<new_shape[2]:
                            #Lack_all[B][A][i+vec[0]][j+vec[1]][k+vec[2]] += vec[3]*int(new_gal[3])
                                key_l = [i+vec[0], j+vec[1], k+vec[2]]
                                key_n = (str(key_l[0:C] + ['Lack'] + key_l[C:B] + ['Lack'] + key_l[B:A] + ['Lack'] + key_l[A:])).strip("[ ]")
                                try:
                                    d43[key_n] += vec[3]*int(new_gal[3])
                                except KeyError :
                                    d43.update({key_n : vec[3]*int(new_gal[3])})


# 3bands source
# aply to three bands
    elif gal.count("Lack")==3 and gal.count("Faint")==0:
        new_gal=list(gal)
        L1=new_gal.index("Lack")
        del new_gal[L1]
        L2=new_gal.index("Lack")
        del new_gal[L2]
        L3=new_gal.index("Lack")
        del new_gal[L3]
        new_shape=list(shape)
        del new_shape[L1],new_shape[L2],new_shape[L3]
        L2=L2+1
        L3=L3+2
        i=int(new_gal[0]);j=int(new_gal[1]);k=int(new_gal[2])
        for v in range(len(th_beam)):
            vec=th_beam[v]
            if 0<=i+vec[0]<new_shape[0] and 0<=j+vec[1]<new_shape[1] and 0<=k+vec[2]<new_shape[2]:
                #Lack_all[L1][L2][i+vec[0]][j+vec[1]][k+vec[2]] += vec[3]*int(new_gal[3])
                key_l = [i+vec[0], j+vec[1], k+vec[2]]
                key_n = (str(key_l[0:L1] + ['Lack'] + key_l[L1:L2] + ['Lack'] + key_l[L2:L3] + ['Lack'] + key_l[L3:])).strip("[ ]")
                try:
                    d33[key_n] += vec[3]*int(new_gal[3])
                except KeyError :
                    d33.update({key_n : vec[3]*int(new_gal[3])})



print("Saving result")
system('mkdir result0.4_plot')
chdir('result0.4_plot')
save("all_detect_grid_Full_6d6",d66)
save("all_detect_grid_Full_6d5",d65)
save("all_detect_grid_Full_6d4",d64)
save("all_detect_grid_Full_6d3",d63)
save("all_detect_grid_Full_5d5",d55)
save("all_detect_grid_Full_5d4",d54)
save("all_detect_grid_Full_5d3",d53)
save("all_detect_grid_Full_4d4",d44)
save("all_detect_grid_Full_4d3",d43)
save("all_detect_grid_Full_3d3",d33)




