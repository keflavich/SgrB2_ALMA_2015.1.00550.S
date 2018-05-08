import os
import numpy as np
import pyregion
from astropy.io import fits
from astropy import log
from astropy import units as u
from astropy.stats import mad_std
import aplpy
import pylab as pl
import radio_beam
import glob
from spectral_cube import SpectralCube
from spectral_cube.lower_dimensional_structures import Projection
import time

for fn in glob.glob("sgr_b2m.[NM].spw*.image.pbcor.fits"):

    #if fits.getheader(fn)['NAXIS'] <= 2:
    #    print("Skipped {0} because it wasn't a cube".format(fn))
    #    continue
    #if os.path.exists('collapse/maxspec/{0}'.format(fn.replace(".image.pbcor.fits","_max_spec.fits"))):
    #    print("Skipped {0} because it is done".format(fn))
    #    continue

    m_or_n = fn.split(".")[1]
    assert m_or_n in ("M","N")

    t0 = time.time()
    log.info("Reading {0}".format(fn))
    cube = SpectralCube.read(fn)
    cube.beam_threshold = 1
    #cube.allow_huge_operations = True
    log.info("Masking out bad beams in {0} ({1}s elapsed)".format(fn, time.time() - t0))
    mcube = cube.mask_out_bad_beams(0.1)
    mcube.beam_threshold = 1

    beam = mcube.beam if hasattr(mcube, 'beam') else mcube.average_beams(1)

    log.info("Max spec ({0}s elapsed)".format(time.time()-t0))
    mxspec = mcube.max(axis=(1,2), how='slice')
    mxspec.write("collapse/maxspec/{0}".format(fn.replace(".image.pbcor.fits", "_max_spec.fits")), overwrite=True)
    mxspec.quicklook("collapse/maxspec/pngs/{0}".format(fn.replace(".image.pbcor.fits", "_max_spec.png")))

    log.info("Avg spec ({0}s elapsed)".format(time.time()-t0))
    reg = pyregion.open('../regions/sgrb2{0}_averaging_region.reg'.format(m_or_n.lower()))
    avspec = mcube.subcube_from_ds9region(reg).mean(axis=(1,2), how='slice')
    avspec_K = (avspec*u.beam).to(u.K, u.brightness_temperature(beam_area=beam,
                                                                disp=mcube.with_spectral_unit(u.GHz).spectral_axis.mean()))

    avspec_K.write("collapse/avspec/{0}".format(fn.replace(".image.pbcor.fits", "_avg_spec_K.fits")), overwrite=True)
    avspec_K.quicklook("collapse/avspec/pngs/{0}".format(fn.replace(".image.pbcor.fits", "_avg_spec_K.png")))

    log.info("Peak intensity ({0}s elapsed)".format(time.time()-t0))
    mx = mcube.max(axis=0, how='slice')
    mx_K = (mx*u.beam).to(u.K, u.brightness_temperature(beam_area=beam,
                                                        disp=mcube.with_spectral_unit(u.GHz).spectral_axis.mean()))
    mx_K.write('collapse/max/{0}'.format(fn.replace(".image.pbcor.fits","_max_K.fits")),
               overwrite=True)
    mx_K.quicklook('collapse/max/pngs/{0}'.format(fn.replace(".image.pbcor.fits","_max_K.png")))


    log.info("Minimum intensity ({0}s elapsed)".format(time.time()-t0))
    mn = mcube.min(axis=0, how='slice')
    mn_K = (mn*u.beam).to(u.K, u.brightness_temperature(beam_area=beam,
                                                        disp=mcube.with_spectral_unit(u.GHz).spectral_axis.mean()))
    mn_K.write('collapse/min/{0}'.format(fn.replace(".image.pbcor.fits","_min_K.fits")),
               overwrite=True)
    mn_K.quicklook('collapse/min/pngs/{0}'.format(fn.replace(".image.pbcor.fits","_min_K.png")))


    for pct in (25,50,75):
        log.info("{1} percentile ({0}s elapsed)".format(time.time()-t0, pct))
        pctmap = mcube.percentile(pct, axis=0, iterate_rays=True)
        beam = mcube.beam if hasattr(mcube, 'beam') else mcube.average_beams(1)
        pctmap_K = (pctmap*u.beam).to(u.K,
                                      u.brightness_temperature(beam_area=beam,
                                                               disp=mcube.with_spectral_unit(u.GHz).spectral_axis.mean()))
        pctmap_K.write('collapse/percentile/{0}'.format(fn.replace(".image.pbcor.fits","_{0}pct_K.fits".format(pct))),
                       overwrite=True)
        pctmap_K.quicklook('collapse/percentile/pngs/{0}'.format(fn.replace(".image.pbcor.fits","_{0}pct_K.png".format(pct))))

    pl.close('all')
