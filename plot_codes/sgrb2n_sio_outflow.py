import os
from astropy import constants, units as u, table, stats, coordinates, wcs, log, coordinates as coord
from astropy.io import fits

from spectral_cube import SpectralCube, Projection

import paths
import files

import pylab as pl


bluefile = paths.Fpath('SgrB2_N_SiO_blue_20to50kms.fits')
redfile = paths.Fpath('SgrB2_N_SiO_blue_77to100kms.fits')
if os.path.exists(bluefile):
    blue = Projection.from_hdu(fits.open(bluefile))
    red = Projection.from_hdu(fits.open(redfile))
else:

    siocube = (SpectralCube
               .read('/Volumes/external/sgrb2/full_SgrB2N_spw0_lines_cutoutN_medsub.fits')
               .with_spectral_unit(u.km/u.s, velocity_convention='radio', rest_value=217.10498*u.GHz)
               .spectral_slab(-200*u.km/u.s, 250*u.km/u.s))
    siocube.spectral_slab(0*u.km/u.s, 120*u.km/u.s).write('SgrB2_N_SiO_medsub_cutout.fits', overwrite=True)

    blue = siocube.spectral_slab(20*u.km/u.s, 50*u.km/u.s).moment0()
    blue.write(bluefile, overwrite=True)

    red = siocube.spectral_slab(77*u.km/u.s, 100*u.km/u.s).moment0()
    red.write(redfile, overwrite=True)

cont_b6 = fits.open(files.contb6_rm2)
cont_b3 = fits.open(files.contb3_rm2)

fig = pl.figure(3)
fig.clf()

ax = fig.add_subplot(111, projection=wcs.WCS(cont_b6[0].header).celestial[2250:-2250,2250:-2250])
ax.imshow(cont_b6[0].data[2250:-2250,2250:-2250],
          origin='lower',
          cmap='gray_r',
          interpolation='none',
         )

ax.contour(blue.value, colors=['b']*10, levels=[0.1,0.2,0.3,0.4,0.5],
           transform=ax.get_transform(blue.wcs))
ax.contour(red.value, colors=['r']*10, levels=[0.1,0.2,0.3,0.4,0.5],
           transform=ax.get_transform(red.wcs))
ax.contour(cont_b3[0].data[2700:-2700, 2700:-2700],
           colors=['y']*10, levels=[0.005, 0.01, 0.02],
           transform=ax.get_transform(wcs.WCS(cont_b3[0].header).celestial[2700:-2700, 2700:-2700]))
ax.axis((476.83561197916686, 1324.4918619791667, 281.24845377604174,
         1316.4047037760415))

fig.savefig(paths.fpath('sgrb2n_sio_outflow.pdf'), bbox_inches='tight')
