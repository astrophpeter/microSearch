import sys
sys.path.append('../skyobj/')
from skyobj import skyobj
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.gridspec as gridspec
from astropy.time import Time
import aplpy
from astropy.io import fits, ascii

def makeplt(lens,source,filename):
	
	minTime = lens.getMinTime(source)
	minDist = lens.getMinDist(source)	

	Ximin,Etamin = lens.getXiEta(minTime)
	XiminS,EtaminS = source.getXiEta(minTime)

	times = np.arange(minTime - 1.0, minTime + 1.0,0.01)
	
	sep = np.array([])		
	posLensXi = np.array([])
	posLensEta = np.array([])
	posSourceXi = np.array([])
	posSourceEta = np.array([])


	for i in times:
		sep = np.append(sep,lens.getSeparation(i,source))

		lensXi,lensEta = lens.getXiEta(i)
		posLensXi = np.append(posLensXi,lensXi)
		posLensEta = np.append(posLensEta,lensEta)

		sourceXi,sourceEta = source.getXiEta(i)
		posSourceXi = np.append(posSourceXi,sourceXi)
		posSourceEta = np.append(posSourceEta,sourceEta)
	

	labelYPos = sep[0] - 100
	labelXPos = minTime
	
	gs = gridspec.GridSpec(1, 2)
	gs.update(wspace=0.5,hspace=0.0)

	ax3 = plt.subplot(gs[0, 0])
	ax2 = plt.subplot(gs[0,1])	
	

	
	ax3.plot(times,sep)
	ax3.scatter(minTime,minDist,label='Minimum')
	ax3.text(labelXPos,labelYPos,r'$t_{min}=$' + str(round(minTime,2)) + ' [yrs]')
	ax3.text(labelXPos,labelYPos - 200,r'$\Delta_{min}=$' + str(round(minDist,2)) + ' [mas]')
	ax3.legend()
	ax3.set_ylabel(r'$\Delta$ Separation [mas]')
	ax3.set_xlabel('Time [Decimal Years]')


	ax2.plot(posLensXi-source.xi_0,posLensEta-source.eta_0,label='Lens Trajectory')
	ax2.scatter(Ximin-source.xi_0,Etamin-source.eta_0,marker="x",label='Lens Closest Pos')
	ax2.scatter(XiminS-source.xi_0,EtaminS-source.eta_0,marker="x",label='Source Closest Pos')
	ax2.plot(posSourceXi-source.xi_0,posSourceEta-source.eta_0,label='Source Trajectory')
	ax2.set_xlabel(r'$\delta \chi$ [mas]')
	ax2.set_ylabel(r'$\delta \eta$ [mas]')
	ax2.legend()
	ax2.axis('equal')

	plt.savefig(filename + '_' + str(lens.id) + '.png',figsize=(14,10),dpi=200)


def makeImplt(lens,source,filename):

	sourceRa  = source.ra_0
	sourceDec = source.dec_0

	minTime = lens.getMinTime(source)
	minDist = lens.getMinDist(source)

	#define cutout image size [arsec]
	imsize = 2

	params = {'ra': sourceRa,'de': sourceDec,'imsize': imsize }

	#DSS Search
	url = "http://stdatu.stsci.edu/cgi-bin/dss_search?v=poss2ukstu_red&r={ra}&d={de}&e=J2000&h={imsize}&w={imsize}&f=fits".format(**params)
	hdulist = fits.open(url)

	#Find the time the image was taken YYYY-MM-DD
	timeString  = hdulist[0].header['DATE-OBS'][:10]
	time = Time(timeString,scale='tcb')
	time.format = 'jyear'

	timedecimal = time.value
	
	sourceRaIm, sourceDecIm = source.getRaDec(timedecimal)
	lensRaIm,lensDecIm = lens.getRaDec(timedecimal)

	sourceRaImC, sourceDecImC = source.getRaDec(minTime)
	lensRaImC,lensDecImC = lens.getRaDec(minTime)

	sourceRaImF,sourceDecImF = source.getRaDec(2035.0)
	lensRaImF,lensDecImF = lens.getRaDec(2035.0)

	lensLine = np.array([[lensRaIm,lensRaImF],[lensDecIm,lensDecImF]])
	sourceLine = np.array([[sourceRaIm,sourceRaImF],[sourceDecIm,sourceDecImF]])


	fig = aplpy.FITSFigure(hdulist[0])
	fig.show_colorscale(cmap='gray_r')

	fig.show_markers(sourceRaIm,sourceDecIm,marker='o',edgecolor='r',label='source')
	fig.show_markers(lensRaIm,lensDecIm,marker='o',edgecolor='b',label='lens')
	fig.show_markers(sourceRaImC,sourceDecImC,marker='*',edgecolor='r',label='source closest')
	fig.show_markers(lensRaImC,lensDecImC,marker='*',edgecolor='b',label='lens closest')

	fig.show_lines([lensLine],color='b',linestyle='--')
	fig.show_lines([sourceLine],color='r',linestyle='--')

	fig.save(filename + '_' + str(lens.id) + '.png',dpi=200)
