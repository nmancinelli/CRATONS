#!/usr/bin/env python
#
def stack_synthetics(syntheticParams):
    # initialize stacked_RF
    from numpy import zeros,arange
    npts=311 #default from Matlab codes
    stacked_RF = zeros(npts)

    rps = syntheticParams["RayParams"]
    ws = syntheticParams["Weights"]

    #Uncomment below for quick, approximate syntethics
    #print '***Warning: These are quick, approximate synthetics'
    #rps = [0.12]
    #ws  = [1.0]

    print 'rps = ', rps

    for irp, RayParam in enumerate(rps):
        w = ws[irp]
        # load synthetic
        depths, RF = load_synthetic_RF_PropMat(RayParam, syntheticParams)

        lenrf=len(RF)

        stacked_RF[:lenrf] = stacked_RF[:lenrf] + w * RF[:lenrf]

    depths=arange(1,npts+1)
    return depths, stacked_RF

def generate_synthetics(syntheticParams, RayParam, ForceNew=False):
    """
    :param syntheticParams:
    :param RayParam:
    :param ForceNew:
    :return:
    """
    from os import chdir, getcwd, system, listdir

    MohoDepth = syntheticParams["MohoDepth"]
    Mohodlnv = syntheticParams["Mohodlnv"]
    PulseWidth = syntheticParams["PulseWidth"]
    LABDepth = syntheticParams["LABDepth"]
    LABdlnv = syntheticParams["LABdlnv"]
    MLDDepth = syntheticParams["MLDDepth"]
    MLDdlnv = syntheticParams["MLDdlnv"]
    LABTransitionThickness = syntheticParams["LABTransitionThickness"]

    print ''
    print 'Working on: RayParam = %.2f ' % RayParam
    print 'Synthetic Params = ', syntheticParams
    print ''


    dir2 = '/Users/mancinelli/PROJECTS/ARRAY_STACK/ReceiverFunctions/Make_Receiver_Functions/CLEAN/Scattered_Waves/SYN/PROPMAT'
    dir1 = getcwd()
    dir3 = '/Users/mancinelli/PROJECTS/ARRAY_STACK/ReceiverFunctions/Make_Receiver_Functions/CLEAN/Scattered_Waves/Data/Projects/Synth_CRATON'

    #Check if syns already exist
    if ForceNew == False:
        chdir('%s/SY_PROPMAT/FAKE/' % (dir3))
        file_name = "RF_Depth_%ds_%ds_%s_%d_%.1f_%.2f_%.1f_%.3f_%d_%.2f_%d_%.2f_%d_%s.mat" % (
            16, 100, "ETMTM", 100, MohoDepth, Mohodlnv, PulseWidth, RayParam,
            LABDepth, LABdlnv, MLDDepth, MLDdlnv, LABTransitionThickness, 'MohoDepth_PulseWidth_UsePostfilter_0')

        files = listdir('./')

        if file_name in files:
            print ''
            print '%s already exists, skipping...' % file_name
            print ''
            chdir(dir1)
            return

        else:
            print '%s not found... ' % (file_name)
            #for each in files:
            #    print each

    chdir(dir2)

    #Write input file
    f = open('test.txt', 'w')
    f.write('5  %.3f  %4.1f\n' % (RayParam, PulseWidth))
    f.write('%4.1f %7.4f %7.4f %7.4f %4.1f %3d\n' % (15., 0.12, 0.12, 0.1083, 20., 10))
    f.write('%4.1f %7.4f %7.4f %7.4f %4.1f %3d\n' % (MohoDepth, Mohodlnv, Mohodlnv*0.785, 0.1655, 0., 1))
    f.write('%4.1f %7.4f %7.4f %7.4f %4.1f %3d\n' % (MLDDepth, MLDdlnv, MLDdlnv, 0., 0., 1))
    f.write('%4.1f %7.4f %7.4f %7.4f %4.1f %3d\n' % (LABDepth, LABdlnv, LABdlnv, 0., LABTransitionThickness, 20))
    f.write('%4.1f %7.4f %7.4f %7.4f %4.1f %3d\n' % (300., 0., 0., 0., 0., 1))
    f.close()

    #Execute matlab code
    system('/Applications/MATLAB_R2016a.app/bin/matlab -nodesktop -nodisplay -r "driveall; exit" > mlab_out.txt ')

    #Now pipe through deconvolution script

    chdir(dir3)

    f=open('exec.bash','w')
    f.write("\n")
    f.write("# !/bin/bash\n")
    f.write("#\n")
    f.write(" # Executes part two of synthetic tests\n")
    f.write("#  (part 1 should be called from within MATLAB IDE)\n")
    f.write("#\n")
    f.write("#\n")
    f.write("/Applications/MATLAB_R2016a.app/bin/matlab -nodesktop -nodisplay << EOF\n")
    f.write("Special_Label = sprintf('MohoDepth_PulseWidth');\n")
    f.write("cd('/Users/mancinelli/PROJECTS/ARRAY_STACK/ReceiverFunctions/Make_Receiver_Functions/CLEAN/Scattered_Waves/Data/Projects/Synth_CRATON');\n")
    f.write("synthetic_test_1_propmat(1,%10f, %10f, %10f, %10f, %10f, %10f, %10f, %10f, %10f, '%s', Special_Label, %d);\n" % (MohoDepth, Mohodlnv, PulseWidth, RayParam, LABDepth, LABdlnv, MLDDepth, MLDdlnv, LABTransitionThickness,'ETMTM', 100))
    f.write("cd('/Users/mancinelli/PROJECTS/ARRAY_STACK/ReceiverFunctions/Make_Receiver_Functions/CLEAN/Scattered_Waves/Data/Projects/Synth_CRATON');\n")
    f.write("synthetic_test_1_propmat(2,%10f, %10f, %10f, %10f, %10f, %10f, %10f, %10f, %10f, '%s', Special_Label, %d);\n" % (MohoDepth, Mohodlnv, PulseWidth, RayParam, LABDepth, LABdlnv, MLDDepth, MLDdlnv, LABTransitionThickness,'ETMTM', 100))
    f.write("EOF\n")
    f.close()

    system('bash exec.bash >> mlab_out.txt')

    chdir(dir1)
    return

def load_synthetic_RF_PropMat(RayParam,syntheticParams):
    """
    This subroutine drives several programs. More documentation to come later.
    :param RayParam:
    :param syntheticParams:
    :return:
    """
    from TOOLS import loadmat
    from numpy import array

    Special_Label = 'MohoDepth_PulseWidth'
    lowT = syntheticParams["lowT"]
    highT = syntheticParams["highT"]
    DeconMethod = syntheticParams["DeconMethod"]
    nIter = syntheticParams["nIter"]
    MohoDepth = syntheticParams["MohoDepth"]
    Mohodlnv = syntheticParams["Mohodlnv"]
    PulseWidth = syntheticParams["PulseWidth"]
    LABDepth = syntheticParams["LABDepth"]
    LABdlnv = syntheticParams["LABdlnv"]
    MLDDepth = syntheticParams["MLDDepth"]
    MLDdlnv = syntheticParams["MLDdlnv"]
    LABTransitionThickness = syntheticParams["LABTransitionThickness"]

    Network = "SY_PROPMAT"

    path2rf = 'Synth_CRATON/%s/FAKE' % (Network)
    file_name = "%s/RF_Depth_%ds_%ds_%s_%d_%.1f_%.2f_%.1f_%.3f_%d_%.2f_%d_%.2f_%d_%s_UsePostfilter_0.mat" % (
        path2rf, lowT, highT, DeconMethod, nIter, MohoDepth, Mohodlnv, PulseWidth, RayParam,
        LABDepth, LABdlnv, MLDDepth, MLDdlnv, LABTransitionThickness, Special_Label)
    print "...loading %s" % (file_name)

    matfile = loadmat(file_name)

    depths = matfile["RF_Depth"][:, 0]
    RFs = matfile["rfs"]

    RF = array(RFs)
    depths = array(depths)

    return depths, RF

# def load_synthetic_RF(RayParam, syntheticParams):
#     from TOOLS import loadmat
#     from numpy import array
#
#     Special_Label = 'MohoDepth_PulseWidth'
#     lowT = syntheticParams["lowT"]
#     highT = syntheticParams["highT"]
#     DeconMethod = syntheticParams["DeconMethod"]
#     nIter = syntheticParams["nIter"]
#     MohoDepth = syntheticParams["MohoDepth"]
#     Mohodlnv = syntheticParams["Mohodlnv"]
#     PulseWidth = syntheticParams["PulseWidth"]
#     LABDepth = syntheticParams["LABDepth"]
#     LABdlnv = syntheticParams["LABdlnv"]
#     MLDDepth = syntheticParams["MLDDepth"]
#     MLDdlnv = syntheticParams["MLDdlnv"]
#     LABTransitionThickness = syntheticParams["LABTransitionThickness"]
#
#     Network = "SY_%d_%.2f_%.1f_%.3f_%d_%.2f_%d_%d_%.2f" % (
#         MohoDepth, Mohodlnv, PulseWidth, RayParam,
#         LABDepth, LABdlnv, LABTransitionThickness, MLDDepth, MLDdlnv)
#
#     Network = Network.replace("." ,"")
#
#     path2rf = 'Synth_CRATON/%s/FAKE' % (Network)
#     file_name = "%s/RF_Depth_%ds_%ds_%s_%d_%.1f_%.2f_%.1f_%.3f_%d_%.2f_%d_%.2f_%d_%s.mat" % (
#         path2rf, lowT, highT, DeconMethod, nIter, MohoDepth, Mohodlnv, PulseWidth, RayParam,
#         LABDepth, LABdlnv, MLDDepth, MLDdlnv, LABTransitionThickness, Special_Label)
#     print "...loading %s" % (file_name)
#
#     matfile = loadmat(file_name)
#
#     depths = matfile["RF_Depth"][:, 0]
#     RFs = matfile["rfs"]
#
#     RF = array(RFs)
#     depths = array(depths)
#
#     return depths, RF