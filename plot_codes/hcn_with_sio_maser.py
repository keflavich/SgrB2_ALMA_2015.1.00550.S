import numpy as np
import os
from astropy import constants, units as u, table, stats, coordinates, wcs, log, coordinates as coord
from astropy.io import fits

from spectral_cube import SpectralCube, Projection

import paths
import files
import regions

import pylab as pl


regs = regions.read_ds9(paths.rpath('sio_masers.reg'))
v2maser = regs[2]

cont_b6 = fits.open(files.contb6_rm2)
cont_b3 = fits.open(files.contb3_rm2)

siov2j2im = paths.Fpath('SiO_v2_j2_peak_N.fits')
if os.path.exists(siov2j2im):
    siov2j2 = Projection.from_hdu(fits.open(siov2j2im))
else:
    region,spw,band,freq = 'N',0,3,85.640452*u.GHz
    fn = paths.eFpath('sgr_b2m.{0}.spw{1}.B{2}.lines.clarkclean1000.robust0.5.image.pbcor.medsub.fits'
                      .format(region, spw, band))
    siov2j2 = (SpectralCube
             .read(fn)
             .with_spectral_unit(u.km/u.s, velocity_convention='radio',
                                 rest_value=freq)
             .spectral_slab(55*u.km/u.s, 110*u.km/u.s)
             .to(u.K)
              ).max(axis=0)
    siov2j2.write(siov2j2im)

hcnv3j1im = paths.Fpath('HCN_v3_j1_peak_N.fits')
if os.path.exists(hcnv3j1im):
    hcnv3j1 = Projection.from_hdu(fits.open(hcnv3j1im))
else:
    region,spw,band,freq = 'N',1,3,88.027223*u.GHz
    fn = paths.eFpath('sgr_b2m.{0}.spw{1}.B{2}.lines.clarkclean1000.robust0.5.image.pbcor.medsub.fits'
                      .format(region, spw, band))
    hcnv3j1 = (SpectralCube
             .read(fn)
             .with_spectral_unit(u.km/u.s, velocity_convention='radio',
                                 rest_value=freq)
             .spectral_slab(55*u.km/u.s, 110*u.km/u.s)
             .to(u.K)
              ).max(axis=0)
    hcnv3j1.write(hcnv3j1im)

hcnv1j1im = paths.Fpath('HCN_v1_j1_peak_N.fits')
if os.path.exists(hcnv1j1im):
    hcnv1j1 = Projection.from_hdu(fits.open(hcnv1j1im))
else:
    region,spw,band,freq = 'N',1,3,88.006629*u.GHz
    fn = paths.eFpath('sgr_b2m.{0}.spw{1}.B{2}.lines.clarkclean1000.robust0.5.image.pbcor.medsub.fits'
                      .format(region, spw, band))
    hcnv1j1 = (SpectralCube
             .read(fn)
             .with_spectral_unit(u.km/u.s, velocity_convention='radio',
                                 rest_value=freq)
             .spectral_slab(55*u.km/u.s, 110*u.km/u.s)
             .to(u.K)
              ).max(axis=0)
    hcnv1j1.write(hcnv1j1im)

fig = pl.figure(3)
fig.clf()

ax = fig.add_subplot(111,
                     projection=wcs.WCS(cont_b6[0].header).celestial[2550:-2550,2550:-2550])
im = ax.imshow(cont_b6[0].data[2550:-2550,2550:-2550], origin='lower',
               cmap='gray_r', interpolation='none',)

cb = pl.colorbar(mappable=im)
cb.set_label("$S_{\\nu}$ [Jy beam$^{-1}$]")

ax.contour(cont_b3[0].data[2700:-2700, 2700:-2700],
           colors=['y']*10, levels=[0.005, 0.01, 0.02],
           linewidths=0.9,
           transform=ax.get_transform(wcs.WCS(cont_b3[0].header).celestial[2700:-2700, 2700:-2700]))
ax.axis((525, 725, 375, 625))

ax.contour(hcnv1j1.value, colors=['lime']*10, levels=[100,150],
           linewidths=0.9,
           transform=ax.get_transform(hcnv1j1.wcs))
ax.contour(hcnv3j1.value, colors=['r']*10, levels=[150,200,250,300,450,500],
           linewidths=0.9,
           transform=ax.get_transform(hcnv3j1.wcs))
ax.contour(siov2j2.value, colors=['c']*10, levels=np.linspace(500,10000,5),
           linewidths=0.9,
           transform=ax.get_transform(siov2j2.wcs))

#ax.plot(v2maser.center.ra, v2maser.center.dec, marker='x', color='w',
#        markersize=7,
#        markeredgewidth=0.5,
#        transform=ax.get_transform('icrs'))

ax.set_xlabel("RA (ICRS)")
ax.set_ylabel("Dec (ICRS)")

fig.savefig(paths.fpath('sgrb2n_sio_maser_and_hcn.pdf'), bbox_inches='tight')


