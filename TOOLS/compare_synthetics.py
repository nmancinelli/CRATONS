#!/usr/bin/env python

def compare_synthetics():
    from matplotlib import pylab as plt

    highT = 100.0

    DM = 'ETMTM'
    outfile = 'synthetic_tests'

    rps = [0.10]
    Weights = [1.0]

    fig = plt.figure(1, figsize=(12, 8))
    for isub, lowT in enumerate([20, 16, 12, 8, 4, 2]):

        ax = plt.subplot(1, 1, 1)
        offset = isub

        plt.plot([offset, offset], [300, 0], 'black')
        tmp = '%d - %d s' % (lowT, highT)
        plt.text(offset, 325, tmp,bbox=dict(facecolor='white', edgecolor='black', boxstyle='round'), fontsize=8,
            horizontalalignment='center')


        if True:
            l1, = add_synthetics(ax, lowT, highT, 30.0, 2.5, rps, Weights,
                                 offset=offset, color='black',
                                 LABDepth=200.0, LABdlnv=0.00, LABTransitionThickness=100,
                                 MLDDepth=80.0, MLDdlnv=0.00,
                                 nIter=100,
                                 DeconMethod=DM,
                                 ls='-')
            l2, = add_synthetics(ax, lowT, highT, 30.0, 2.5, rps, Weights,
                                 offset=offset, color='blue',
                                 LABDepth=200.0, LABdlnv=0.05, LABTransitionThickness=100,
                                 MLDDepth=80.0, MLDdlnv=0.00,
                                 nIter=100,
                                 DeconMethod=DM,
                                 ls='--')
            l3, = add_synthetics(ax, lowT, highT, 30.0, 2.5, rps, Weights,
                                 offset=offset, color='red',
                                 LABDepth=200.0, LABdlnv=0.00, LABTransitionThickness=100,
                                 MLDDepth=80.0, MLDdlnv=0.05,
                                 nIter=100,
                                 DeconMethod=DM,
                                 ls='--')

            l4, = add_synthetics(ax, lowT, highT, 30.0, 2.5, rps, Weights,
                                 offset=offset, color='magenta',
                                 LABDepth=200.0, LABdlnv=0.05, LABTransitionThickness=100,
                                 MLDDepth=80.0, MLDdlnv=0.05,
                                 nIter=100,
                                 DeconMethod=DM,
                                 ls='--')

    plt.legend([l1, l2, l3, l4], ['null', 'LAB (gradual)', 'MLD (sharp)', 'LAB + MLD'], loc='lower right')

    ax.set_ylim([0.0, 310.0])
    ax.set_xlim([-1, 8])
    ax.set_xticks([])

    plt.ylabel('Depth (km)')
    plt.gca().invert_yaxis()

    plt.title('Synthetic RF Comparison')

    plt.savefig(outfile)

    print 'Finished with %s ' % (outfile)
    return


def add_synthetics(ax, lowT, highT, MohoDepth, PulseWidth, RayParams, Weights,
                   LABDepth=200.0, LABdlnv=-0.0, LABTransitionThickness=1.0,
                   MLDDepth=80.0, MLDdlnv=10.0,
                   DeconMethod='ETMTM',
                   nIter=100,
                   offset=0.0,
                   color='black',
                   label='',
                   ls='--'):
    from numpy import add
    from TOOLS import stack_synthetics
    depths, RF = stack_synthetics(
        RayParams, Weights, lowT, highT, MohoDepth, PulseWidth,
        LABDepth=LABDepth, LABdlnv=LABdlnv,  MLDDepth=MLDDepth, MLDdlnv=MLDdlnv,
        LABTransitionThickness=LABTransitionThickness, DeconMethod=DeconMethod, nIter=nIter)

    scale = 100.0
    if lowT > 10:
        scale = scale * 2.0

    if DeconMethod == 'ITDD':
        scale = scale * 1.6

    from numpy import array
    refline = array(depths) * 0. + array(offset)  # plot everything wrt this line

    tmp = RF * scale

    xs = tmp + refline

    l0 = ax.plot(xs, depths, ls=ls, color=color, linewidth=2.0, label=label)

    return l0
