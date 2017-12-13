import sys
sys.path.append('../skyobj/')
from skyobj import skyobj
import plotutils as plot
lens = skyobj(id=1,ra=67.80238,dec=58.97810,pmra=1.336*1000.0,pmdec=-1.936*1000.0,parallax=0,epoch=2000.0)

source = skyobj(id=2,ra=67.81246,dec=58.97045,pmra=0.0,pmdec=0.0,parallax=0.0,epoch=2000.0)


lensppmxl = skyobj(id=1,ra=176.428838,dec=-64.841519,pmra=2665.7,pmdec=-347.2,parallax=0,epoch=2000.0)

sourceppmxl = skyobj(id=2,ra=176.463694,dec=-64.843343,pmra=-19.5,pmdec=-17.8,epoch=2000.0,parallax=0.0)

print(lensppmxl.getMinTime(sourceppmxl))
print(lensppmxl.getMinDist(sourceppmxl))


plot.makeplt(lensppmxl,sourceppmxl,'ppmxltraj')
plot.makeImplt(lensppmxl,sourceppmxl,'ppmxltest')
