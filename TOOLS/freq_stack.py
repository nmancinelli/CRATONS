#!/usr/bin/env python
def freq_stack():
    global nboot, RSqStore, stname, RFstack, RFstack_mean, RFstack_std
    from matplotlib import pylab as plt
    from stack_synthetics import generate_synthetics

    DeconMethod, highT, path2rf, outfile, baz1, baz2, SNR_min, \
    nboot, Taup_Misfit_Min, Taup_Misfit_Max, average_type, allSyntheticParams = parse_inline_input()

    tmp = path2rf[0].split('/')[-1]

    #Manually change if you want to calc. goodness of fit
    CalculateGoodnessOfFit=False
    RSqStore={}

    #Dump information for the GRL publication
    if True:
        FileForPub = open('ForPub.txt', 'a')
        FileForPub.write('# \n')
        FileForPub.write('# %s \n' % tmp)
        FileForPub.write('# \n')

    #Prepare synthetics - uncomment this if new synthetics need to be generated
    #for SyntheticParams in allSyntheticParams:
    #    for RayParam in [0.09, 0.092, 0.094, 0.096, 0.098, 0.1, 0.102, 0.104, 0.106, 0.108, 0.11, 0.112, 0.114, 0.116, 0.118]:
        #for RayParam in [0.12]:
    #        generate_synthetics(SyntheticParams, RayParam)

    fig = plt.figure(1, figsize=(3.5, 1.75))
    params = {'legend.fontsize': 4,
              'figure.figsize': (3, 1.5),
              'axes.labelsize': 5,
              'axes.titlesize': 7,
              'figure.titlesize': 7,
              'figure.dpi': 500,
              'xtick.labelsize': 5,
              'ytick.labelsize': 5}
    plt.rcParams.update(params)

    #For the GRL paper, the goodness-of-fit calculation was carried out only at 16s

    if CalculateGoodnessOfFit:
        ListOfPeriods = [16]
    else:
        ListOfPeriods = [20, 16, 12, 8, 4, 2]

    for isub, lowT in enumerate(ListOfPeriods):

        rect1 = [0.1, 0.15, 0.7, 0.8]
        rect2 = [0.82, 0.15, 0.1, 0.8]
        ax = fig.add_axes(rect1)
        ax4 = fig.add_axes(rect2)
        offset = isub

        if True:
            lenRFs, RPs, BAZIs, depths, NRFs = multi_station_stack(ax, ax4, path2rf, lowT, highT,
                                                     offset=offset,
                                                     label='%.0f-%.0f s' % (lowT, highT),
                                                     baz1=baz1,
                                                     baz2=baz2, SNR_min=SNR_min,
                                                     Taup_Misfit_Min=Taup_Misfit_Min,
                                                     Taup_Misfit_Max=Taup_Misfit_Max,
                                                     average_type=average_type,
                                                     DeconMethod=DeconMethod)
                                                     
            frp=open('RP_BAZI/file.txt','w')
            for itmp,tmp in enumerate(RPs):
                frp.write('%f  %f\n' % (RPs[itmp], BAZIs[itmp]))
                
            frp.close()    
            

        if True:
            from numpy import histogram, arange, sum
            bin_edges = arange(0.09, 0.122, 0.002)

            Weights, bin_edges = histogram(RPs,bins=bin_edges,density=True)
            Weights = Weights/sum(Weights)

            rps = bin_edges[:-1]

            lines = []
            labels = []
            syns = []

            for isyn in range(len(allSyntheticParams)):
                SyntheticParams = allSyntheticParams[isyn]
                SyntheticParams["DeconMethod"] = DeconMethod
                SyntheticParams["RayParams"] = rps
                SyntheticParams["Weights"] = Weights
                SyntheticParams["offset"] = offset
                SyntheticParams["nIter"] = 100 # for ITDD only
                SyntheticParams["lowT"] = lowT
                SyntheticParams["highT"] = highT
                #l0, RFsyn = add_synthetics(ax, SyntheticParams, Rescale=True)

                #lines.append(l0)
                #labels.append(SyntheticParams["label"])
                #syns.append(RFsyn)

        if CalculateGoodnessOfFit:
            if lowT == 16.:
                for ii in range(len(depths)):
                    from numpy import shape
                    #print shape(depths), shape(RFstack), shape(RFstack_std), shape(syns)
                    #FileForPub.write('%6.1f  %e  %e  %e  %e  %e  %e\n' %
                    # (depths[ii], RFstack_mean[ii], RFstack_std[ii], syns[0][ii], syns[1][ii], syns[2][ii], syns[3][ii]))

                    FileForPub.write('%6.1f  %e  %e  ' % (depths[ii], RFstack_mean[ii], RFstack_std[ii]))
                    for isyn in range(len(syns)):
                        FileForPub.write('%e  ' % (syns[isyn][ii]))
                    FileForPub.write('\n')

    if False:
        if len(allSyntheticParams)>0:
            ax.legend(lines,labels)

    ax4.fill_betweenx(depths, NRFs, x2=0.0, facecolor='lightblue')

    ylims=[0., 310.]
    ax.set_ylim(ylims)
    ax4.set_ylim(ylims)
    ax.set_xlim([-1, 8])
    ax.set_xticks([])

    ax.set_ylabel('Depth (km)')
    ax.invert_yaxis()
    ax4.invert_yaxis()
    ax4.set_yticklabels([])
    ax4.set_xlim(0, lenRFs*1.25)
    ax4.set_xticks([0, lenRFs])
    ax4.set_xlabel('RFs used\nin stack')

    if False:
        plt.suptitle('%s\n%d Receiver Functions -- SNR > %.1f -- nboot = %d -- Average: %s -- %s' % (
            path2rf, lenRFs, SNR_min, nboot, average_type, DeconMethod))

    if True:
        left, bottom, width, height = [0.62, 0.50, 0.15, 0.15]
        ax2 = fig.add_axes([left, bottom, width, height])
        (n, bins, patches) = ax2.hist(RPs)
        plt.annotate('Frequency', xy=(-0.25,0.5), xycoords='axes fraction', fontsize=3, rotation=90,va='center')
        plt.annotate('Ray Parameter (s/km)', xy=(0.5,-0.47), xycoords='axes fraction', fontsize=3,ha='center')
        plt.locator_params(axis='y', nbins=4)
        plt.locator_params(axis='x', nbins=5)
        plt.xlim([0.09, 0.120])

        left, bottom, width, height = [0.62, 0.25, 0.15, 0.15]
        ax3 = fig.add_axes([left, bottom, width, height])
        ax3.hist(BAZIs)
        plt.annotate('Frequency', xy=(-0.25,0.5), xycoords='axes fraction', fontsize=3, rotation=90, va='center')
        plt.annotate('Backazimuth (degrees)', xy=(0.5,-0.47), xycoords='axes fraction', fontsize=3, ha='center')
        plt.locator_params(axis='y', nbins=4)
        plt.locator_params(axis='x', nbins=5)
        plt.xlim([-180, 180])
        plt.xticks([-180,-60,60,180])

        for ax in [ax2, ax3]:
            for item in ([ax.title, ax.xaxis.label, ax.yaxis.label] +
                             ax.get_xticklabels() + ax.get_yticklabels()):
                item.set_fontsize(3)

            plt.setp(ax.xaxis.get_majorticklabels(), rotation=0)
            plt.setp(ax.yaxis.get_majorticklabels(), rotation=0)

            for tick in ax.yaxis.get_majorticklabels():
                tick.set_x(+0.09)
            for tick in ax.xaxis.get_majorticklabels():
                tick.set_y(+0.18)
                tick.set_rotation(45)

    plt.savefig(outfile)


    #
    #
    #
    if CalculateGoodnessOfFit:
        nsyn=len(allSyntheticParams)
        #
        fout=open('RSq_%s.out' % stname,'w')
        #
        fout.write('%d  %d\n' % (nsyn,nboot))
        for iboot in range(nboot):
            tmpa=iboot
            fout.write('%5d   ' % tmpa)
            for isyn in range(1,nsyn+1):
                tmpb=RSqStore[(isyn, 16, iboot)]
                fout.write('%7e   ' % tmpb)
            fout.write('\n')

            #tmpstr = '%5d  %7e   %7e   %7e   %7e\n' % (tmpa, tmpb, tmpc, tmpd, tmpe)
            #fout.write(tmpstr)
        fout.close()

        fout=open('Model_List.out','w')
        for isyn in range(nsyn):
            tmp=allSyntheticParams[isyn]
            tmpa,tmpb,tmpc=tmp["LABDepth"], tmp["LABdlnv"], tmp["LABTransitionThickness"]
            fout.write('%f  %f  %f\n' % (tmpa,tmpb,tmpc) )
        fout.close()


    print 'Finished with %s ' % (outfile)
    return

def add_synthetics(ax, syntheticParams, Rescale=False):
    from matplotlib import pylab as plt

    global RFstack, RFstack_mean, nboot, RSqStore, RFstack_std
    from TOOLS import stack_synthetics
    from scipy.stats import linregress

    depths, RF = stack_synthetics(syntheticParams)

    scale = 6.5
    if syntheticParams["lowT"] > 10:
        scale = scale * 1.0

    if syntheticParams["DeconMethod"] == 'ITDD':
        scale = scale * 2.0

    refline = depths * 0. + syntheticParams["offset"]  # plot everything wrt this line

    # Enhance deep
    from numpy import array
    RF = RF*scale
    RFstack_meanScl = RFstack_mean * scale
    RFstack_stdScl = RFstack_std * scale
    RFstackScl = RFstack * scale

    if Rescale:
        phi, _, _, _, _ = linregress(RF, RFstack_meanScl)
        print 'rescaling by factor %f' % (phi)
        RF = RF * phi

    tmp = RF

    xs = tmp+refline

    l0 = ax.plot(xs, depths, ls=syntheticParams["LineStyle"], color=syntheticParams["Color"], linewidth=0.5)

    for iboot in range(nboot):
        mask = (depths > 150.0) * (depths < 250.0)
        RSq = sum((RF - RFstackScl[iboot,:])**2 / (RFstack_stdScl)**2 * mask)
        RSq = RSq / sum(mask)

        #plt.figure(13)
        #plt.plot(RFstackScl[iboot,:] - RFstack_stdScl)
        #plt.plot(RFstackScl[iboot,:] + RFstack_stdScl)
        #plt.plot(RF,'--')
        #plt.show()

        key=(syntheticParams["isyn"],syntheticParams["lowT"],iboot)
        RSqStore[key]=RSq
        #print key, RSq

    return l0, RF / scale

def multi_station_stack(ax, ax4, path2rf, lowT, highT,
                        offset=0.0, label='', scale_bar=False, baz1=-999.0, baz2=999.0,
                        SNR_min=0.0, Taup_Misfit_Min=-9999., Taup_Misfit_Max=9999.,
                        average_type='mean', DeconMethod='none'):
    global RFstack_mean, RFstack, RFstack_std, nboot, stname
    from TOOLS import loadmat
    from numpy import zeros, isnan, std, mean, nanstd
    RFs_all = []
    RPs_all = []
    BAZIs_all = []
    SNRs_all = []

    for each_path2rf in path2rf:

        file_name = '%s/RF_Depth_%ds_%ds_%s_UsePostfilter_0.mat' % (each_path2rf, lowT, highT, DeconMethod)

        print '...loading %s' % (file_name)

        ###Open SNR file

        SNR = []
        Taup_Misfit = []

        snrfile = '%s/SNR_%ds_%ds.txt' % (each_path2rf, lowT, highT)
        file = open(snrfile)
        print "...%s snrfile loaded" % (snrfile)
        for line in file.readlines():
            nfo = line.strip('\n').split()
            SNR.append(float(nfo[1]))
            Taup_Misfit.append(float(nfo[2]))
        file.close()

        ###Get matfile
        matfile = loadmat(file_name)
        print "...%s matfile loaded" % (file_name)

        RFs = matfile["rfs"][:, :]

        stdRF0 = nanstd(RFs, axis=0)

        BAZIs = matfile["BAZIsave"][:]
        RPs = matfile["RPsave"][:]
        depths = matfile["RF_Depth"][:, 0]
        meanRF0 = matfile["RF_Depth"][:, 1]

        # check for bad snrfile
        if len(SNR) != len(RFs):
            print '***Warning: len(SNR) != len(RFs) , %d , %d ' % (len(SNR), len(RFs))
            dum = raw_input('Press enter to continue')

        stname = path2rf[0].split('/')[-1]

        #This is for printing data for bazi RFs
        if False:
            fout = open('%s_%02ds.txt' % (stname, lowT), 'w')

            for ii in range(len(RFs)):
                fout.write('%7f %7f \n' % (BAZIs[ii], SNR[ii]))
                tmp = RFs[ii]
                for jj in range(len(tmp)):
                    fout.write('   %10e\n' % (tmp[jj]))

            fout.close()


        # cull out undesirables
        for ii in range(len(RFs)):
            if BAZIs[ii] >= baz1 and BAZIs[ii] <= baz2 and \
                            SNR[ii] >= SNR_min and \
                            Taup_Misfit[ii] >= Taup_Misfit_Min and Taup_Misfit[ii] <= Taup_Misfit_Max:
                #
                # check if RF deviates far from mean RF - Emily's method

                ndev = 0
                for idep in range(len(depths)):
                    if RFs[ii, idep] > meanRF0[idep] + 1.0 * stdRF0[idep] or \
                                    RFs[ii, idep] < meanRF0[idep] - 1.0 * stdRF0[idep]:
                        ndev = ndev + 1

                determ = float(ndev) / float(len(depths))
                if determ < 0.75:
                    RFs_all.append(RFs[ii])
                    RPs_all.append(RPs[ii])
                    BAZIs_all.append(BAZIs[ii])
                    SNRs_all.append(SNR[ii])


    ### Estimate spatial coherence
    #from TOOLS import estimate_spatial_coherence
    #station=path2rf[0].split('/')[-1]
    #Dmin, Dmax = 150.0, 250.0
    #estimate_spatial_coherence(RFs_all, RPs_all, BAZIs_all, depths, Dmin, Dmax,
    #                           outfile='SPATCOH/spatcoh_%s_%ds_%dkm_%dkm.txt' % (station, lowT, Dmin, Dmax))

    #fdump=open('out.datadump','w')
    #
    #fdump.write('%d\n' % len(RFs_all))

    #for ii,tmp in enumerate(RFs_all):
    #    header = '%10f   %10f   %10f\n' % (RPs_all[ii], BAZIs_all[ii], SNRs_all[ii])
    #    fdump.write(header)
    #    for eachval in tmp:
    #        fdump.write('%-10.3e   ' % (eachval))
    #
    #    fdump.write('\n')
    #
    #fdump.close()

    #Dmin, Dmax = 80.0, 150.0
    #estimate_spatial_coherence(RFs_all, RPs_all, BAZIs_all, depths, Dmin, Dmax,
    #                           outfile='SPATCOH/spatcoh_%s_%ds_%dkm_%dkm.txt' % (station, lowT, Dmin, Dmax))

    #Dmin, Dmax = 150.0, 250.0
    #estimate_spatial_coherence(RFs_all, RPs_all, BAZIs_all, depths, Dmin, Dmax,
    #                           outfile='SPATCOH/spatcoh_%s_%ds_%dkm_%dkm.txt' % (station, lowT, Dmin, Dmax))

    ### Begin stacking and bootstrapping
    RFstack = zeros(nboot * len(RFs_all[0])).reshape(nboot, len(RFs_all[0]))

    NRFs = []

    ## New section
    from numpy import nanmedian, shape, nanmean
    NRF, NDEP = shape(RFs_all)

    tmp=zeros(NRF*NDEP).reshape(NRF,NDEP)

    for ii in range(NRF):
        for jj in range(NDEP):
            tmp[ii,jj] = RFs_all[ii][jj]

    from numpy.random import randint
    for iboot in range(nboot):
        resamp=zeros(NRF*NDEP).reshape(NRF,NDEP)
        for ii in range(NRF):
            index=randint(0, NRF-1)
            resamp[ii,:]=tmp[index,:]
        if average_type == 'median':
            RFstack[iboot, :] = nanmedian(resamp,axis=0)
        elif average_type == 'mean':
            RFstack[iboot, :] = nanmean(resamp, axis=0)
        else:
            from sys import exit
            exit('Error: bad average type')


    for idep, depth in enumerate(depths):
         amp_at_dep = []  # list containing RF amps at depth
         for iRF in range(len(RFs_all)):
             if not isnan(RFs_all[iRF][idep]):
                 amp_at_dep.append(RFs_all[iRF][idep])
    #
         NRF = len(amp_at_dep)
         NRFs.append(NRF)
    #
    #     for iboot in range(nboot):
    #         if average_type == 'mean':
    #             RFstack[iboot, idep] = mean(choice(amp_at_dep, NRF))
    #         elif average_type == 'median':
    #             RFstack[iboot, idep] = median(choice(amp_at_dep, NRF))
    #         elif average_type == 'tmean':
    #             tmp_m = mean(choice(amp_at_dep, NRF))
    #             tmp_std = std(choice(amp_at_dep, NRF))
    #             lwr = tmp_m - 2.0 * tmp_std
    #             upr = tmp_m + 2.0 * tmp_std
    #             tmp_tm = tmean(choice(amp_at_dep, NRF), limits=(lwr, upr))
    #             RFstack[iboot, idep] = tmp_tm

    RFstack_mean = mean(RFstack, axis=0)
    RFstack_std = std(RFstack, axis=0)

    refline = depths * 0. + offset  # plot everything wrt this line

    scale = 6.0
    if lowT > 10:
        scale = scale * 1.0

    if DeconMethod == 'ITDD':
        scale = scale * 2.0

    ax.plot(refline, depths, '--', color='black', linewidth=0.2)

    nsigma = 2.0
    fmin = (RFstack_mean - nsigma * RFstack_std) * scale + refline
    fmax = (RFstack_mean + nsigma * RFstack_std) * scale + refline
    ax.fill_betweenx(depths, fmin, fmax, facecolor='gray', edgecolor='None')
    fmin = RFstack_mean * 0.0 + refline
    fmax = (RFstack_mean - nsigma * RFstack_std) * scale + refline
    ax.fill_betweenx(depths, fmin, fmax, where=fmax > fmin, facecolor='red', edgecolor='None')
    fmax = RFstack_mean * 0.0 + refline
    fmin = (RFstack_mean + nsigma * RFstack_std) * scale + refline
    ax.fill_betweenx(depths, fmin, fmax, where=fmax > fmin, facecolor='blue', edgecolor='None')

    ax.text(refline[0], 330, label, fontsize=5,
            horizontalalignment='center',rotation=30.0)

    #Scale Bar
    if True:
        ls=6.7
        rs=ls+ scale * 0.1
        ys=45.
        ax.plot([ls, rs], [ys, ys],linewidth=1, color='black')
        ax.text((ls+rs)/2.,ys-5.,'10% parent\namplitude', ha='center', weight='light', style='italic', fontsize=3.5)

        ax.annotate(stname, xy=(0.01,0.05) ,xycoords='axes fraction', weight='bold',fontsize=5)

    return len(RFs_all), RPs_all, BAZIs_all, depths, NRFs

def parse_inline_input():

    # These are the stacking params
    DeconMethod = raw_input('Deconvolution Method (ETMTM): \n').split()[0]
    highT = float(raw_input('High T in seconds (100): \n').split()[0])
    numsta = int(raw_input('Number of channels (1): \n').split()[0])

    path2rf=[]
    tmp = raw_input('Path for channels (separated by spaces): \n').split()
    for ista in range(numsta):
        path2rf.append(tmp[ista])

    outfile = raw_input('Outfile: \n').split()[0]
    baz1, baz2 = raw_input('Baz1, Baz2: \n').split()[0:2]
    baz1,baz2 = float(baz1), float(baz2)
    SNR_min = float(raw_input('SNR Min: \n').split()[0])
    nboot = int(raw_input('Nboot: \n').split()[0])
    Taup_Misfit_Min, Taup_Misfit_Max = raw_input('Taup Misfit Min, Max: \n').split()[0:2]
    Taup_Misfit_Min, Taup_Misfit_Max = float(Taup_Misfit_Min), float(Taup_Misfit_Max)
    average_type = raw_input('Average Type (median): \n').split()[0]

    #Put synthetic params in a list of dictionary
    numsyn = int(raw_input('Number of synthetics (0): \n').split()[0])

    allSyntheticParams=[]

    for isyn in range(numsyn):
        tmp={}
        a,b = raw_input('Moho: Depth (km), Fractional Velocity Jump \n').split()[0:2]
        tmp["MohoDepth"], tmp["Mohodlnv"] = float(a), float(b)
        a,b   = raw_input('MLD: Depth (km), Fractional Velocity Jump \n').split()[0:2]
        tmp["MLDDepth"], tmp["MLDdlnv"] = float(a), float(b)
        a,b,c  = raw_input('LAB: Depth (km), Fractional Velocity Jump \n').split()[0:3]
        print a,b,c
        tmp["LABDepth"], tmp["LABdlnv"], tmp["LABTransitionThickness"] = float(a), float(b), float(c)
        tmp["PulseWidth"] = float(raw_input('Pulse Width (s) \n').split()[0])
        a,b = raw_input('Line Style and Color (- black): \n').split()[0:2]
        tmp['LineStyle']=a
        tmp['Color']=b
        tmp['label'] = raw_input('Line label: \n')
        tmp['propMat'] = True
        tmp['isyn'] = isyn + 1  #python counts from 0
        allSyntheticParams.append(tmp)

    return DeconMethod, highT, path2rf, outfile, baz1, baz2,\
           SNR_min, nboot, Taup_Misfit_Min, Taup_Misfit_Max, average_type, \
           allSyntheticParams

def write_depth_integrated_variance(RFstack_std, SNR_min):
    fout = open('depth_integrated_variance.txt', 'a')
    text = 'Depth-integrated variance, SNR_min = %f, %f\n' % (sum(RFstack_std), SNR_min)
    fout.write(text)
    fout.close()

    return

def parse_user_input_old():
    from sys import argv

    inputs = argv
    dummy = inputs.pop(0)
    DeconMethod = inputs.pop(0)
    # use popleft to take one arg at a time

    highT = float(inputs.pop(0))

    # print inputs
    numsta = int(inputs.pop(0))

    path2rf = []
    for ista in range(numsta):
        path2rf.append(inputs.pop(0))

    outfile = inputs.pop(0)

    baz1 = float(inputs.pop(0))
    baz2 = float(inputs.pop(0))
    SNR_min = float(inputs.pop(0))
    nboot = int(inputs.pop(0))
    Taup_Misfit_Min = float(inputs.pop(0))
    Taup_Misfit_Max = float(inputs.pop(0))
    average_type = inputs.pop(0)

    # print 'Saving to %s ' % (outfile)

    return DeconMethod, highT, path2rf, outfile, baz1, baz2, SNR_min, nboot, Taup_Misfit_Min, Taup_Misfit_Max, average_type
