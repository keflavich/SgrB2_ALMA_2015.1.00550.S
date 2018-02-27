import paths
from astropy import units as u
from astropy.io import fits
from astropy import coordinates
import radio_beam

for fn in ('SgrB2_B3_continuum_QA2_minimumcutout.fits',
           'sgr_b2m.N.allspw.continuum.clean1000.image.tt0.pbcor.fits',
           'sgr_b2m.N.B6.allspw.continuum.r-2.cleanto2mJy_2terms.image.tt0.pbcor.fits',
           #'sgr_b2m.M.B3.allspw.continuum.r-2.dirty.image.tt0.pbcor.fits',
           'sgr_b2m.N.B3.allspw.continuum.r-2.dirty.image.tt0.pbcor.fits',
           #'sgr_b2m.M.B3.allspw.continuum.r0.5.clean1000.image.tt0.pbcor.fits',
           #'sgr_b2m.N.B3.allspw.continuum.r0.5.clean1000.image.tt0.pbcor.fits',
           #'sgr_b2m.M.B3.allspw.continuum.r-2.clean1000.image.tt0.pbcor.fits',
          ):

    fh = fits.open(paths.Fpath(fn))

    if fh[0].header['RADESYS'] == 'FK5':
        refcen = coordinates.SkyCoord(fh[0].header['CRVAL1']*u.deg,
                                      fh[0].header['CRVAL2']*u.deg,
                                      frame='fk5').icrs
        fh[0].header['CRVAL1'] = refcen.ra.deg
        fh[0].header['CRVAL2'] = refcen.dec.deg
        fh[0].header['RADESYS'] = 'ICRS'

    beam = radio_beam.Beam.from_fits_header(fh[0].header)

    fh[0].data = (fh[0].data * beam.jtok(fh[0].header['CRVAL3']*u.Hz)).value

    fh.writeto(paths.Fpath(fn.replace(".fits","_K.fits")), overwrite=True)
