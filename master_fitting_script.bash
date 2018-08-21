#!/bin/bash
MOHODROP=0.19
#
#  bash stack_net_sta.bash  45 0.28 8  II 1 NRIL
#  bash stack_net_sta.bash  40 ${MOHODROP} 8  II 2 OBN  OBN10
  bash stack_net_sta.bash  43 ${MOHODROP} 6  II 2 BRVK BRVK10    #FIG4
  bash stack_net_sta.bash  40 ${MOHODROP} 8  II 1 ARU            #FIG4
  bash stack_net_sta.bash  30 ${MOHODROP} 12 II 2 ALE  ALE10     #FIG4
#  bash stack_net_sta.bash  40 0.25 8  II 2 FFC  FFC10
  bash stack_net_sta.bash  40 ${MOHODROP} 8  II 1 LVZ            #FIG4
  bash stack_net_sta.bash  40 ${MOHODROP} 8  II 2 WRAB WRAB10    #FIG4
##
##
  bash stack_net_sta.bash 40 ${MOHODROP} 8 IU 2 RSSD RSSD10      #FIG4
#  bash stack_net_sta.bash 50 0.25 12 IU 3 CCM   CCM00  CCM10
#  bash stack_net_sta.bash 55 0.30 12 IU 2 WCI00 WCI10
#  bash stack_net_sta.bash 40 0.30 8 IU 2 PTGA  PTGA00
#  bash stack_net_sta.bash 35 0.30 8 IU 2   KOWA00 KOWA10
#  bash stack_net_sta.bash 35 0.30 8 IU 2 MBWA   MBWA10
#  bash stack_net_sta.bash 45 0.30 12 IU 1 NWAO   #NWAO00 NWAO10
#  bash stack_net_sta.bash 40 0.20 8 IU 1 RCBR
#  bash stack_net_sta.bash 40 0.20 8 IU 2 TRQA  TRQA10
##
##
#  bash stack_net_sta.bash 58 0.25 8 GE 1 MHV
#  bash stack_net_sta.bash 50 0.25 12 GE 1 PUL
#  bash stack_net_sta.bash 50 0.25 8 GE 1 TRTE
##
##
#  bash stack_net_sta.bash 50 0.25 8 US 2 EGMT EGMT00
#  bash stack_net_sta.bash 53 0.25 8 US 2 LAO  LAO00
#  bash stack_net_sta.bash 57 0.25 8 US 4 DGMT DGMT00 DGMT10 DGMTHR
#  bash stack_net_sta.bash 47 0.25 8 US 2 OGNE OGNE00
#  bash stack_net_sta.bash 45 0.25 7 US 2 CBKS CBKS00
#  bash stack_net_sta.bash 45 0.25 8 US 4 KSU1 KSU100 KSU110 KSU1HR
#  bash stack_net_sta.bash 50 0.25 8 US 2 SCIA SCIA00
  bash stack_net_sta.bash 43 ${MOHODROP} 12 US 4 ECSD ECSD00 ECSD10 ECSDHR   #FIG4
#  bash stack_net_sta.bash 54 0.25 8 US 2 HDIL HDIL00
#  bash stack_net_sta.bash 45 0.25 8 US 4 JFWS JFWS00 JFWS10 JFWSHR
#  bash stack_net_sta.bash 45 0.25 8 US 2 COWI COWI00
  bash stack_net_sta.bash 35 ${MOHODROP} 8 US 4 EYMN EYMN00 EYMN10 EYMNHR    #FIG4
#  bash stack_net_sta.bash 43 0.25 8 US 2 AGMN AGMN00
#  bash stack_net_sta.bash 50 0.25 8 US 2 GLMI GLMI00
#  bash stack_net_sta.bash 55 0.25 8 US 2 ACSO ACSO00
##AU
#   bash stack_net_sta.bash 35 0.25 8 AU 1 ARMA
#   bash stack_net_sta.bash 45 0.25 8 AU 1 BBOO
#   bash stack_net_sta.bash 35 0.25 7 AU 1 COEN
#   bash stack_net_sta.bash 37 0.25 8 AU 1 EIDS
#   bash stack_net_sta.bash 40 0.25 8 AU 1 FITZ
#   bash stack_net_sta.bash 40 0.25 8 AU 1 KMBL
#   bash stack_net_sta.bash 40 0.25 7 AU 1 STKA
#   bash stack_net_sta.bash 35 0.25 7 AU 1 TOO
#   bash stack_net_sta.bash 35 0.25 7 AU 1 YNG
#
##CN
   bash stack_net_sta.bash 35 ${MOHODROP} 8 CN 5 YKW1 YKW2 YKW3 YKW4 YKW5    #FIG4
##BL
#   bash stack_net_sta.bash 35 0.25 7 BL 1 CRJB
#   bash stack_net_sta.bash 35 0.25 7 BL 1 ITPB
#   bash stack_net_sta.bash 35 0.25 7 BL 1 PDCB
#   bash stack_net_sta.bash 35 0.25 7 BL 1 SNVB
#   bash stack_net_sta.bash 35 0.25 7 BL 1 STMB
##AF
#   bash stack_net_sta.bash 35 0.25 7 AF 1 BLWY
#   bash stack_net_sta.bash 35 0.25 7 AF 1 BOBN
#   bash stack_net_sta.bash 35 0.25 7 AF 1 CVNA
#   bash stack_net_sta.bash 35 0.25 7 AF 1 DODT
#  bash stack_net_sta.bash 35 0.25 7 AF 1 GETA
#  bash stack_net_sta.bash 35 0.25 7 AF 1 GRM
#   bash stack_net_sta.bash 35 0.25 7 AF 1 HARE
#   bash stack_net_sta.bash 35 0.25 7 AF 1 HVD
#   bash stack_net_sta.bash 35 0.25 7 AF 1 KIG
#   bash stack_net_sta.bash 45 0.25 7 AF 1 KTWE
#   bash stack_net_sta.bash 35 0.25 7 AF 1 LBB
#   bash stack_net_sta.bash 35 0.25 7 AF 1 MBEY
#   bash stack_net_sta.bash 35 0.25 7 AF 1 MONG
#   bash stack_net_sta.bash 35 0.25 7 AF 1 MOPA
#   bash stack_net_sta.bash 35 0.25 7 AF 1 MTVE
#   bash stack_net_sta.bash 35 0.25 7 AF 1 MZM
#   bash stack_net_sta.bash 35 0.25 7 AF 1 NBI
#   bash stack_net_sta.bash 35 0.25 7 AF 1 PKA
#   bash stack_net_sta.bash 35 0.25 7 AF 1 POGA
#   bash stack_net_sta.bash 35 0.25 7 AF 1 PWET
#   bash stack_net_sta.bash 35 0.25 7 AF 1 RUDU
#   bash stack_net_sta.bash 35 0.25 7 AF 1 SEK
#   bash stack_net_sta.bash 35 0.25 7 AF 1 SOE
#   bash stack_net_sta.bash 35 0.25 7 AF 1 SWZ
#   bash stack_net_sta.bash 35 0.25 7 AF 1 TEBE
#   bash stack_net_sta.bash 35 0.25 7 AF 1 TETE
#   bash stack_net_sta.bash 35 0.25 7 AF 1 TEZI
#   bash stack_net_sta.bash 35 0.25 7 AF 1 UPI
#   bash stack_net_sta.bash 35 0.25 7 AF 1 WIN
#   bash stack_net_sta.bash 35 0.25 7 AF 1 ZOMB
#
## GT
#
   bash stack_net_sta.bash 35 ${MOHODROP} 7 GT 2 BOSA BOSA00    #FIG4
#   bash stack_net_sta.bash 40 0.25 7 GT 2 DBIC DBIC00
#   bash stack_net_sta.bash 45 0.25 7 GT 2 LBTB LBTB00