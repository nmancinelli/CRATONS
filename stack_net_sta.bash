#!/bin/bash
#
# The master fitting script calls this.

MOHODEPTH=${1}
MOHODROP=${2}
PW=${3}
AZI1=-180
AZI2=180
NET=${4}
NCHAN=${5}
STA1=${6}
STA2=${7}
STA3=${8}
STA4=${9}
STA5=${10}

CHAN1=CRATON/${NET}/${STA1}
CHAN2=CRATON/${NET}/${STA2}
CHAN3=CRATON/${NET}/${STA3}
CHAN4=CRATON/${NET}/${STA4}
CHAN5=CRATON/${NET}/${STA5}

echo working on ${NET} ${STA1} ${STA2} ${STA3} ${STA4} ${STA5}

for DMETH in ETMTM; do

for AVGTYPE in median; do

for SNR in 2; do

cat << !! > subscript.bash
python call_freq_stack.py << ! #> /dev/null &
${DMETH}  #Deconvolution Method (ETMTM)
100       #High T in seconds (100)
${NCHAN}         #Number of channels (1 thru 5)
${CHAN1} ${CHAN2} ${CHAN3} ${CHAN4} ${CHAN5}  #Path for channels (separated by spaces, 5 max)
OUT/${STA1}.SNR.${SNR}.${AVGTYPE}.${DMETH}.eps #Outfile
${AZI1} ${AZI2}     #Baz1, Baz2
${SNR}              # SNR Min
100                # nboot (100)
-9 +9    #Taup Misfit Min, Max
${AVGTYPE}          #Average Type (median)
!!

##Search over synthetics
DEPTHS=(150 175 200 225 250)
VJUMPS=(-0.03 -0.05 -0.10)
WIDTHS=(0 20 40 80 160)

##No synthetics
#DEPTHS=()
#VJUMPS=()
#WIDTHS=()

NA=${#DEPTHS[@]}
NB=${#VJUMPS[@]}
NC=${#WIDTHS[@]}

echo $NA $NB $NC
NSYN=$(($NA * $NB * $NC + 1))
#NSYN=$(($NA * $NB * $NC))

cat << !!! >> subscript.bash
${NSYN}                   #Number of synthetics to add (0)
!!!

cat << !!!!! >> subscript.bash
$MOHODEPTH $MOHODROP   #Moho: Depth (km), Fractional Velocity Jump
100  -0.00             #MLD: Depth (km), Fractional velocity Drop
200  +0.00 40        #LAB: Depth (km), Fractional velocity Drop, Width (km)
6                   #PulseWidth (s)
-- black            #Line style and color (- black)
0pct
!!!!!

for EACHDEPTH in ${DEPTHS[*]}; do
for VELJUMP in ${VJUMPS[*]}; do
for WIDTH in ${WIDTHS[*]}; do
cat << !!!! >> subscript.bash
$MOHODEPTH $MOHODROP   #Moho: Depth (km), Fractional Velocity Jump
100  -0.00             #MLD: Depth (km), Fractional velocity Drop
${EACHDEPTH} ${VELJUMP} ${WIDTH}        #LAB: Depth (km), Fractional velocity Drop, Width (km)
6                   #PulseWidth (s)
-- black            #Line style and color (- black)
label               #label
!!!!
done
done
done

bash subscript.bash

done

done

done