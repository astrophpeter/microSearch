import sys
sys.path.append('../skyobj/')
from skyobj import skyobj
from astropy.table import Table
import plotutils as plot

TGASPATH = '/Users/petermcgill/Desktop/tgas_source.fits'
XMATCHPATH = '/Users/petermcgill/Desktop/HSOYGAIAsourceXmatch.fits'
RUNPATH = 'run3/'

data = Table.read(XMATCHPATH)

#remove duplicate lens source pairs
dupmask = (data['source_id'] != data['gaia_id'])
data = data[dupmask]

#candmask = data['source_id'] == 3235238026141505280
#data = data[candmask]
#sourcemask = data['gaia_id'] == 3235238026144043136
#data = data[sourcemask]

print("Number of lens/source pairs to be checked: " +str(data['source_id']))

temp = sys.stdout
sys.stdout = open(RUNPATH + 'results.txt', "a")
print ("Lens_id,Source_id,MinDist,Mintime,0.1MsolShift,0.5MsolShift,1.0MsolShift")
sys.stdout.close()

#iterate over all XMATCH
for i in range(0,len(data['source_id'])):
	sys.stdout = temp
	print(i)
	
	#print("lens pmra" + str(data['pmra'][i]))
	#print("lens pmdec" + str(data['pmdec'][i]))

	source = skyobj(id=data['source_id'][i],ra=data['ra'][i],
               dec=data['dec'][i],pmdec=0.0,pmra=0.0,epoch=2015.0,parallax=0.0)

	#lens = skyobj(id=data['source_id'][i],ra=data['ra'][i],
	#	dec=data['dec'][i],pmra=data['pmra'][i],pmdec=data['pmdec'][i],
	#	epoch=data['ref_epoch'][i],parallax=data['parallax'][i])

	lens = skyobj(id=data['gaia_id'][i],ra=data['raj2000'][i],
		dec=data['dej2000'][i],epoch=2000.0,
		pmra=(data['pmra'][i]*3600.0*1000.0),pmdec=(data['pmde'][i]*3600.0*1000.0),parallax=0)

	try:
		minTime = lens.getMinTime(source)
	except:
		minTime = 0.0
		pass
	
	if (minTime > 2018.0 and  minTime < 2025.0):		
		
		try:
			minDist = lens.getMinDist(source)
		except:
			minDist = 0.0
			pass			
		
		if (minDist < 700.0):
			
			#plot.makeImplt(lens,source,'newcand.png')
			sys.stdout = open(RUNPATH + 'results.txt', "a")	
	
			print(str(lens.id) + ',' + str(source.id) + ',' + str(minDist) + ',' + str(minTime) + ',' + str(lens.getCentroidShift(source,0.1)) + ',' + str(lens.getCentroidShift(source,0.5)) + ',' + str(lens.getCentroidShift(source,1.0)))

			sys.stdout.close()

	

