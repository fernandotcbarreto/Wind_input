import numpy as np
from netCDF4 import Dataset as dat
import xarray as xr

tgtbase='saida'
#ufile='/mnt/c/Users/fernando.barreto/Downloads/eranovdec.nc'
#vfile='/mnt/c/Users/fernando.barreto/Downloads/eranovdec.nc'
ufile='/mnt/c/Users/fernando.barreto/Downloads/previsao_vento_u_20231027.nc'
vfile='/mnt/c/Users/fernando.barreto/Downloads/previsao_vento_v_20231027.nc'

file=xr.open_dataset(vfile)

unet=dat(ufile)

vnet=dat(vfile)

intervalu = int( np.diff(unet['time'][::])[0]*24 )

intervalv = int( np.diff(vnet['time'][::])[0]*24 )


u=np.squeeze(unet['ugrd10m'][::])

v=np.squeeze(vnet['vgrd10m'][::])

#uwnd = tgtbase+'_era_5_ND'+'.amu'

#vwnd = tgtbase+'_era_5_ND'+'.amv'

uwnd = tgtbase+'_era_5_JJ'+'.amu'

vwnd = tgtbase+'_era_5_JJ'+'.amv'

lonu = unet['lon'][::]-360
latu = unet['lat'][::]
lonv = vnet['lon'][::]-360
latv = vnet['lat'][::]

dlatu=np.diff(latu)

dlonu=np.diff(lonu)

dlatv=np.diff(latv)

dlonv=np.diff(lonv)

if (dlatu[0] < 0):
  dlatu=dlatu*(-1)
  dlatv=dlatv*(-1)


ufid = open(uwnd,'w');
vfid = open(vwnd,'w');

ufid.write('FileVersion      = 1.03\n')
vfid.write('FileVersion      = 1.03\n')

ufid.write('Filetype         = meteo_on_equidistant_grid\n')
vfid.write('Filetype         = meteo_on_equidistant_grid\n')

ufid.write('NODATA_value         = -999.000\n')
vfid.write('NODATA_value         = -999.000\n')

ufid.write('n_cols           = %d\n' %(u.shape[2]) )

vfid.write('n_cols           = %d\n' %(v.shape[2]) )


ufid.write('n_rows           = %d\n' %(u.shape[1]) )

vfid.write('n_rows           = %d\n' %(v.shape[1]) )

ufid.write('grid_unit        = degree\n')

vfid.write('grid_unit        = degree\n')


ufid.write('x_llcorner       = %f\n' %(lonu.min()) )

vfid.write('x_llcorner       = %f\n' %(lonv.min()) )


ufid.write('dx               = %f\n'% (dlonu[0]))

vfid.write('dx               = %f\n'% (dlonv[0]))


ufid.write('y_llcorner       = %f\n' %(latu.min()) )

vfid.write('y_llcorner       = %f\n' %(latv.min()) )


ufid.write('dy               = %f\n'% (dlatu[0]))

vfid.write('dy               = %f\n'% (dlatv[0]))

ufid.write('n_quantity       = 1\n')
vfid.write('n_quantity       = 1\n')

ufid.write('quantity1        = x_wind\n')

vfid.write('quantity1        = y_wind\n')

ufid.write('unit1            = m s-1\n')
vfid.write('unit1            = m s-1\n')

[ntu,niu,nju] = u.shape;

[ntv,niv,njv] = v.shape;

c=0

for t in range(ntu):
#  ufid.write('TIME = ' +str(c)+ ' hours since 2022-11-01 00:00:00 +00:00\n')
  ufid.write('TIME = ' +str(c)+ ' hours since 2023-10-27 06:00:00 +00:00\n')
  for i in range(niu):
     for j in range(nju):
       ufid.write('%9.3f'%(u[t,i,j]))
     ufid.write('\n')  
  c=c+intervalu

ufid.close()

c=0
for t in range(ntv):
#  vfid.write('TIME = ' +str(c)+ ' hours since 2022-11-01 00:00:00 +00:00\n')
  vfid.write('TIME = ' +str(c)+ ' hours since 2023-10-27 06:00:00 +00:00\n')
  for i in range(niv):
     for j in range(njv):
       vfid.write('%9.3f'%(v[t,i,j]))
     vfid.write('\n')  
  c=c+intervalv

vfid.close()