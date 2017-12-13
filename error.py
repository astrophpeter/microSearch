#source pm from ppmxl, everyting else from gaia dr1

#info for lawd37 event

import numpy as np
import matplotlib.pyplot as plt
import sys
sys.path.append('../skyobj/')
from skyobj import skyobj


MAS_TO_DEG = (1.0 / 3600.0*1000.0)
NUMS = 10000

lensRa = 176.4549073
lensRaerr = 0.17862226 * MAS_TO_DEG
lensDec = -64.84295714
lensDecerr = 0.22230826 * MAS_TO_DEG
lenspmra = 2662.03572627
lenspmraerr = 0.15470192
lenspmdec = -345.18255501
lenspmdecerr = 0.15334393
lensparallax = 215.7823335
lensparallaxerr = 0.2727838
sourceRa = 176.46360456
sourceRaerr = 1.54734795 * MAS_TO_DEG
sourceDec = -64.84329779
sourceDecerr = 2.29809596 * MAS_TO_DEG
sourcepmra = -19.5
sourcepmraerr = 9.39999962 
sourcepmdec = -17.89999962
sourcepmdecerr = 9.39999962


lens_ra_samples = np.random.normal(loc=lensRa, scale=lensRaerr, size=NUMS)
lens_dec_samples = np.random.normal(loc=lensDec, scale=lensDecerr, size=NUMS)
lens_pmra_samples = np.random.normal(loc=lenspmra, scale=lenspmraerr, size=NUMS)
lens_pmdec_samples = np.random.normal(loc=lenspmdec, scale=lenspmdecerr, size=NUMS)
lens_parallax_samples = np.random.normal(loc=lensparallax, scale=lensparallaxerr, size=NUMS)

source_ra_samples = np.random.normal(loc=sourceRa, scale=sourceRaerr, size=NUMS)
source_dec_samples = np.random.normal(loc=sourceDec, scale=sourceDecerr, size=NUMS)
source_pmra_samples = np.random.normal(loc=sourcepmra, scale=sourcepmraerr, size=NUMS)
source_pmdec_samples = np.random.normal(loc=sourcepmdec, scale=sourcepmdecerr, size=NUMS)

time = np.zeros(NUMS)

for i in range(0,NUMS):

	lens = skyobj(id=1,ra=lens_ra_samples[i],dec=lens_dec_samples[i],
		pmra=lens_pmra_samples[i],pmdec=lens_pmdec_samples[i],epoch=2015.0,
		parallax=-lens_parallax_samples[i])
	source = skyobj(id=1,ra=source_ra_samples[i],dec=source_dec_samples[i],
                pmra=source_pmra_samples[i],pmdec=source_pmdec_samples[i],epoch=2015.0,
                parallax=0)

	time[i] = lens.getMinTime(source)



print(time)


plt.hist(time,bins=100)
plt.show()
