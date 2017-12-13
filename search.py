import sys
sys.path.append('../skyobj/')
from skyobj import skyobj
from astropy.table import Table
import plotutils as plot

TGASPATH = '/Users/petermcgill/Desktop/tgas_source.fits'
XMATCHPATH = '/Users/petermcgill/Proft2012/data/TGASandGaiaSource.fits'
RUNPATH = 'run1/'

data = Table.read(XMATCHPATH)

#remove duplicate lens source pairs
dupmask = (data['source_id'] != data['source_id_cone'])
data = data[dupmask]

#total = 0


mask = (data['source_id_cone'] == 5332606346467258496)
data = data[mask]

#print(len(data['source_id']))



#sys.stdout = open(RUNPATH + 'results.txt', "w")
print ("Lens_id,Source_id,MinDist,Mintime,0.1MsolShift,0.5MsolShift,1.0MsolShift")

#iterate over all XMATCH
for i in range(0,len(data['source_id'])):
	
	lens = skyobj(id=data['source_id'][i],ra=data['ra'][i],
		dec=data['dec'][i],pmra=data['pmra'][i],pmdec=data['pmdec'][i],
		epoch=data['ref_epoch'][i],parallax=-data['parallax'][i])

	source = skyobj(id=data['source_id_cone'][i],ra=data['ra_cone'][i],
		dec=data['dec_cone'][i],epoch=2015.0,
		pmra=-19.5,pmdec=-17.90,parallax=0)

	minTime = lens.getMinTime(source)	
	print(lens.getETime(source,0.75))
	
	if (minTime > 2018.0 and  minTime < 2025.0):
		minDist = lens.getMinDist(source)
		
		if (minDist < 700.0):
			print(str(lens.id) + ',' + str(source.id) + ',' + str(minDist) + ',' + str(minTime) + ',' + str(lens.getCentroidShift(source,0.1)) + ',' + str(lens.getCentroidShift(source,0.5)) + ',' + str(lens.getCentroidShift(source,1.0)))
			#plot.makeplt(lens,source,RUNPATH + 'tangentplane/TGAS')
			#plot.makeImplt(lens,source,RUNPATH + 'image/TGAS')


