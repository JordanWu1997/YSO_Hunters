#!/usr/bin/env python
from sys import argv

if len(argv) != 3:
    print("Error\nto_c2d_format.py [original catalog] [output catalog]")

catalog=open(argv[-2])
#catalog=catalog.readlines()[13:]

output=open(argv[-1],'w')
#head=open('headline','r')
#head=head.read()
#output.write(head)

for line in catalog:
	
        list=[0 for i in range(0,233)]
        #print(len(line.split()))
        ra=line.split()[2]
        dra=line.split()[3]
        dec=line.split()[4]
        ddec=line.split()[5]
        #--------------------
        
        Prob_Galc=line.split()[9]
        obtype=line.split()[16]
        
        #--------------------
        J=line.split()[21]
        dJ=line.split()[22]
        QJ=line.split()[24]
        H=line.split()[25]
        dH=line.split()[26]
        QH=line.split()[28]
        K=line.split()[29]
        dK=line.split()[30]
        QK=line.split()[32]
        IR1=line.split()[41]
        dIR1=line.split()[42]
        QIR1=line.split()[44]
	imIR1=line.split()[46]
        IR2=line.split()[59]
        dIR2=line.split()[60]
        QIR2=line.split()[62]
	imIR2=line.split()[64]
        IR3=line.split()[77]
        dIR3=line.split()[78]
        QIR3=line.split()[80]
	imIR3=line.split()[82]
        IR4=line.split()[95]
        dIR4=line.split()[96]
        QIR4=line.split()[98]
	imIR4=line.split()[100]
        MP1=line.split()[113]
        dMP1=line.split()[114]
        QMP1=line.split()[116]
	imMP1=line.split()[118]
        MP2=line.split()[131]
        dMP2=line.split()[132]
        QMP2=line.split()[134]
	imMP2=line.split()[136]
	list[0]=str(ra)
        list[1]=str(dra)
        list[2]=str(dec)
        list[3]=str(ddec)
        #---------------------
        
        list[11]=str(Prob_Galc)
        list[16]=str(obtype)
        
        #---------------------
        list[33]=str(J)
        list[34]=str(dJ)
        list[37]=str(QJ)
        list[54]=str(H)
        list[55]=str(dH)
        list[58]=str(QH)
        list[75]=str(K)
        list[76]=str(dK)
        list[79]=str(QK)
        list[96]=str(IR1)
        list[97]=str(dIR1)
        list[100]=str(QIR1)
	list[102]=str(imIR1)
        list[117]=str(IR2)
        list[118]=str(dIR2)
        list[121]=str(QIR2)
	list[123]=str(imIR2)
        list[138]=str(IR3)
        list[139]=str(dIR3)
        list[142]=str(QIR3)
	list[144]=str(imIR3)
        list[159]=str(IR4)
        list[160]=str(dIR4)
        list[163]=str(QIR4)
	list[165]=str(imIR4)
        list[180]=str(MP1)
        list[181]=str(dMP1)
        list[184]=str(QMP1)
	list[186]=str(imMP1)
        list[201]=str(MP2)
        list[202]=str(dMP2)
        list[205]=str(QMP2)
	list[207]=str(imMP2)
	
	line=ra
	for i in range(1,233):
		line = line + "\t" + str(list[i])
	line=line + "\n"
	output.write(line)
