
import paths
from astropy import units as u
from astropy.io import fits
from astropy import wcs
import reproject

b3 = fits.open(paths.Fpath('SgrB2_B3_continuum_QA2_minimumcutout_K.fits'))
b6 = fits.open(paths.Fpath('sgr_b2m.N.allspw.continuum.clean1000.image.tt0.pbcor_K.fits'))

b3r,_ = reproject.reproject_interp(input_data=(b3[0].data.squeeze(),
                                               wcs.WCS(b3[0].header).celestial),
                                   output_projection=wcs.WCS(b6[0].header).celestial,
                                   shape_out=b6[0].data.shape
                                  )

ratio = b3r / b6[0].data.squeeze()

ratiohdu = fits.PrimaryHDU(data=ratio, header=b6[0].header)
ratiohdu.writeto(paths.Fpath('ratio_B3toB6_N.fits'), overwrite=True)
