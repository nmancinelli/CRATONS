#!/usr/bin/env python
#
#
def main():
	from matplotlib import rcParams
	from matplotlib import pylab as plt
	from sys import argv
	from numpy import sum,arange,mean,std,zeros
	from numpy.random import rand
	
	highT=30.0

	path2rf=argv[1]
	
	print 'Looking in %s ' % (path2rf)
	
	outfile=argv[2]
	nbins=int(argv[3])
	SNR_min=float(argv[4])
	bin_by=int(argv[5])
	bazi0=float(argv[6])
	bazi1=float(argv[7])
	
	print 'Saving to %s ' % (outfile)

	fig=plt.figure(1,figsize=(4,8))
	for isub,lowT in enumerate([8,4,1]):
		
		ax=plt.subplot2grid((3, 10), (isub, 0) ,colspan=8)
		
		out,dep1,dep2=stack_by_azimuth(ax,path2rf,lowT,highT,SNR_min=SNR_min,bin_by=bin_by,nbins=nbins,bazi0=bazi0,bazi1=bazi1)
		plt.title('%s: Low T = %.1f' % (path2rf, lowT))
		
		## A little experimental section using PCA -- crashes in the case of an empty column
		#from matplotlib.mlab import PCA
		#print out
		#results = PCA(out.T)
		#plt.imshow(results.Y,aspect='auto',cmap='RdBu_r',origin='upper',interpolation='nearest')
		#plt.figure(77)
		#plt.plot(results.Y[:,:1])
		#plt.show()
		#return
		#RFPCA=results.Y[:,0]+results.Y[:,1]
		##
		
		nboot=100
		RFstack=zeros(nboot*len(out[0,:])).reshape(nboot,len(out[0,:]))
	
		nbins=len(out[:,0])
	
		for iboot in range(nboot):
			for iRF in range(nbins):
				iran=int(rand()*nbins)
				RFstack[iboot,:]=RFstack[iboot,:]+out[iran,:]
			
		RFmean=mean(RFstack,axis=0)
		RFstd=std(RFstack,axis=0)
	
		ax2=plt.subplot2grid((3, 10), (isub, 8) , colspan = 2)
		
		ax2.plot(RFmean,-arange(len(RFmean)))
		depths=-arange(len(RFmean))
		fmin=RFmean+RFstd
		fmax=RFmean-RFstd
		
		ax2.fill_betweenx(depths,fmin,fmax,facecolor='lightgray',edgecolor='None')
		
		fmin=RFmean*0.0
		fmax=(RFmean-RFstd)
	
		ax2.fill_betweenx(depths,fmin,fmax,where= fmax>fmin, facecolor='red',edgecolor='None')
	
		fmax=RFmean*0.0 
		fmin=(RFmean+RFstd)
	
		ax2.fill_betweenx(depths,fmin,fmax,where= fmax>fmin,facecolor='blue',edgecolor='None')
		
		ax2.set_ylim([-dep2,dep1])
		ax2.set_yticklabels([])
		scale=int(max(abs(RFmean))/2.)
		ax2.set_xticks([-scale,+scale])
		ax2.set_xlim([-scale*3.0,+scale*3.0])
		ax2.set_title('Sum')
		ax2.set_xlabel('RF Amplitude')

	rcParams.update({'font.size': 6})

	#plt.subplots_adjust(wspace=None)
	plt.tight_layout()
	plt.savefig(outfile)
	
	print 'Finished with %s ' % (outfile)
	return
	
def stack_by_azimuth(ax,path2rf,lowT,highT,SNR_min=0.0,bin_by=1,nbins=10,bazi0=-180.0,bazi1=180.0):
	"""
	"""
	from matplotlib import pylab as plt
	from sys import path
	path.append('/Users/mancinelli/PROG/SUBS/PYTHON/')
	from loadmat import loadmat
	from numpy import zeros,isnan,std,mean
	from numpy.random import rand
	
	RFs_all=[]
	RPs_all=[]
	BAZIs_all=[]

	path=path

	if lowT<1.0:
		file_name='%s/RF_Depth_%.1fs_%ds.mat' % (path2rf,lowT,highT)
	else:
		file_name='%s/RF_Depth_%ds_%ds.mat' % (path2rf,lowT,highT)

	print '...loading %s' % (file_name)
	
	snr_limit=True;
	if snr_limit:
		snrfile='%s/SNR_%ds.txt' % (path2rf,lowT)
		file=open(snrfile)
		SNR=[]
		for line in file.readlines():
			nfo=line.strip('\n').split()
			SNR.append(float(nfo[1]))
		file.close()

	matfile = loadmat(file_name)

	RFs = matfile["rfs"][:,:]
	
	BAZIs= matfile["BAZIsave"][:]
	RPs= matfile["RPsave"][:]
	depths = matfile["RF_Depth"][:,0]
	
	if len(SNR) != len(RFs):
		print '***Warning: len(SNR) != len(RFs) , %d , %d ' % (len(SNR), len(RFs))
		dum=raw_input('Press enter to continue')
		
	tmp1,tmp2,tmp3=[],[],[]
	for ii in range(len(RFs)):
		if SNR[ii]>SNR_min:
			
			tmp1.append(RFs[ii])
			tmp2.append(RPs[ii])
			tmp3.append(BAZIs[ii])
			
	RFs=tmp1
	RPs=tmp2
	BAZIs=tmp3
	
	if bin_by == 1:
		x1=bazi1
		x0=bazi0
		xlist=BAZIs
	else:
		x0=min(RPs)*0.98
		x1=max(RPs)*1.02
		xlist=RPs
	
	stack=zeros(nbins*len(RFs[0])).reshape(nbins,len(RFs[0]))
	Nstack=zeros(nbins*len(RFs[0])).reshape(nbins,len(RFs[0]))
	
	for iRF,RF in enumerate(RFs):
		x=xlist[iRF]
		ibin=int( (x-x0) / (x1-x0) *nbins)
		if ibin < 0 or ibin > (nbins-1):
			print '***Warning ibin out of range, skipping...'
			continue
		for jj in range(len(RFs[0])):
			if isnan(RF[jj]) == False:
				stack[ibin,jj]=stack[ibin,jj]+RF[jj]
				Nstack[ibin,jj]=Nstack[ibin,jj]+1
		
	for ibin in range(nbins):
		for jj in range(len(RFs[0])):
			if Nstack[ibin,jj]>0.:
				stack[ibin,jj]=stack[ibin,jj]/Nstack[ibin,jj]
				
	#demean and renorm
	for ibin in range(nbins):
		#stack[ibin,:]=stack[ibin,:]-mean(stack[ibin,:])
		norm = max(abs(stack[ibin,:]))
		if norm>0.0:
			stack[ibin,:]=stack[ibin,:]/norm
	
	
	y2=min(depths)
	y1=max(depths)
	
	ax.imshow(stack.T,aspect='auto',cmap='RdBu_r',origin='upper',interpolation='nearest',extent=[x0,x1,y1,y2])
	
	if bin_by==1:
		plt.xlabel('Back Azimuth (degrees)')
	else:
		plt.xlabel('Ray Parameter (s/km)')
	
	plt.ylabel('Depth (km)')
		
	return stack,y2,y1
	
main()
