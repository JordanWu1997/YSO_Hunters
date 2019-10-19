#! bin/python
from pylab import *
from numpy import *
from sys import argv
from os import system, chdir

sigma= 2 #(Grid unit i.e integers)
bond=7
cube="0.2(mag)"
# 6band
six_band_beam=[]
for i in range(-bond,1+bond):
    for j in range(-bond,1+bond):
        for k in range(-bond,1+bond):
            for l in range(-bond,1+bond):
                for m in range(-bond,1+bond):
                    for n in range(-bond,1+bond):
                        r_sqa=float(i**2+j**2+k**2+l**2+m**2+n**2)
                        G=exp(-(r_sqa/(2*sigma**2)))
                        if r_sqa<=bond**2:
                            vec=[i,j,k,l,m,n,G]
                            six_band_beam.append(vec)

fig0=[]
for i in range(len(six_band_beam)):
    if six_band_beam[i][0]==0 and six_band_beam[i][1]==0 and six_band_beam[i][2]==0 and six_band_beam[i][3]==0 and six_band_beam[i][4]==0:
        fig0.append(six_band_beam[i][6])
# 5band
five_band_beam=[]
for i in range(-bond,1+bond):
   for j in range(-bond,1+bond):
      for k in range(-bond,1+bond):
         for l in range(-bond,1+bond):
            for m in range(-bond,1+bond):
               r_sqa=float(i**2+j**2+k**2+l**2+m**2)
               G=exp(-(r_sqa/(2*(sigma*(5.0/6.0)**0.5)**2)))
               if r_sqa<=bond**2:
                  vec=[i,j,k,l,m,G]
                  five_band_beam.append(vec)
fig1=[]
for i in range(len(five_band_beam)):
    if five_band_beam[i][0]==0 and five_band_beam[i][1]==0 and five_band_beam[i][2]==0 and five_band_beam[i][3]==0:
        fig1.append(five_band_beam[i][5])

# 4band
four_band_beam=[]
for i in range(-bond,1+bond):
   for j in range(-bond,1+bond):
      for k in range(-bond,1+bond):
         for l in range(-bond,1+bond):
            r_sqa=float(i**2+j**2+k**2+l**2)
            G=exp(-(r_sqa/(2*(sigma*(4.0/6.0)**0.5)**2)))
            if r_sqa<=bond**2:
                vec=[i,j,k,l,G]
                four_band_beam.append(vec)
fig2=[]
for i in range(len(four_band_beam)):
    if four_band_beam[i][0]==0 and four_band_beam[i][1]==0 and four_band_beam[i][2]==0:
        fig2.append(four_band_beam[i][4])

# 3band
three_band_beam=[]
for i in range(-bond,1+bond):
   for j in range(-bond,1+bond):
      for k in range(-bond,1+bond):
            r_sqa=float(i**2+j**2+k**2)
            G=exp(-(r_sqa/(2*(sigma*(3.0/6.0)**0.5)**2)))
            if r_sqa<=bond**2:
                vec=[i,j,k,G]
                three_band_beam.append(vec)
fig3=[]
for i in range(len(three_band_beam)):
    if three_band_beam[i][0]==0 and three_band_beam[i][1]==0:
        fig3.append(three_band_beam[i][3])

#plot figure
XX=[]
for i in range(-bond,1+bond):
    XX.append(float(i+0.5))
plot(XX,fig0,ls='steps')
plot(XX,fig1,ls='steps')
plot(XX,fig2,ls='steps')
plot(XX,fig3,ls='steps')
print(fig0)
print(fig1)
print(fig2)
print(fig3)
xlabel("cube"+cube)
ylabel("counts")
system('mkdir GPV_result_sigma' + str(sigma))
chdir('GPV_result_sigma' + str(sigma))
system('mkdir ND_Beam_sigma' + str(sigma))
chdir('ND_Beam_sigma' + str(sigma))
savefig("Beam_in_diff_dim")
#~~~~~~~~~~~~~~~~~~~~``
save('6d_beam_sigma'+str(sigma),six_band_beam)
save('5d_beam_sigma'+str(sigma),five_band_beam)
save('4d_beam_sigma'+str(sigma),four_band_beam)
save('3d_beam_sigma'+str(sigma),three_band_beam)

