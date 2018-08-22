#!usr/bin/env python
#
def estimate_spatial_coherence(RFs, RPs, BAZIs, Depths, Dmin, Dmax, outfile='spatcoh.txt'):
    print "Estimating spatial coherence..."
    from numpy import array
    Depths=array(Depths)
    mask = ((Depths) < Dmax) * 1 * ((Depths) > Dmin) * 1

    fout=open(outfile,'w')
    for ii in range(len(RFs)):
        for jj in range(len(RFs)):
            #Don't compare with self or double count
            if ii >= jj:
                continue

            RF1=RFs[ii]
            RF2=RFs[jj]

            RF1=RF1*mask
            RF2=RF2*mask

            #for kk in range(len(RF1)):
            #    if Depths[kk] > Dmax or Depths[kk] < Dmin:
            #        RF1[kk], RF2[kk] = 0.,0.
            #    #print '%10f  %10f  %10f' % (RF1[kk], RF2[kk], Depths[kk])

            #RF1=RF1[Depths >= Dmin]
            #RF2=RF2[Depths >= Dmin]
            #Depths=Depths[Depths >= Dmin]
            #RF1=RF1[Depths <= Dmax]
            #RF2=RF2[Depths <= Dmax]
            #Depths=Depths[Depths <= Dmax]

            RP1=RPs[ii]
            RP2=RPs[jj]
            BAZI1=BAZIs[ii]
            BAZI2=BAZIs[jj]

            N = compute_norm(RF1, RF2)
            D = compute_distance_measure(RP1, BAZI1, RP2, BAZI2)

            tmp = '%10E %10E\n' % (D,N)
            fout.write(tmp)

    fout.close()
    return

def compute_norm(A,B):
    from numpy import sqrt
    tmp=A-B
    tmp=tmp**2.
    tmp=sum(tmp)
    tmp=sqrt(tmp)
    return tmp

def compute_distance_measure(r1,the1,r2,the2):
    from numpy import cos, pi, sqrt

    dthe = (the2-the1)*pi/180.

    #Dsq  = r1**2 + r2**2 - 2.*r1*r2*cos(dthe)

    #D = sqrt(Dsq)

    if dthe > pi:
        dthe=dthe - 2.*pi
    if dthe < -pi:
        dthe=dthe + 2.*pi

    return dthe
