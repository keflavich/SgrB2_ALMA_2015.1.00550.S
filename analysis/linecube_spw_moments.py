import os
import numpy as np
from astropy.io import fits
from astropy import units as u
from astropy.stats import mad_std
import aplpy
import pylab as pl
import radio_beam
import glob
from spectral_cube import SpectralCube
from spectral_cube.lower_dimensional_structures import Projection

for fn in glob.glob("sgr_b2m.[NM].spw*.image.pbcor.fits"):
    if fits.getdata(fn).ndim <= 2:
        print("Skipped {0} because it wasn't a cube".format(fn))
        continue
    if os.path.exists('collapse/max/{0}'.format(fn.replace(".image.pbcor.fits","_max_K.fits"))):
        print("Skipped {0} because it is done".format(fn))
        continue

    cube = SpectralCube.read(fn)
    cube.beam_threshold = 1
    cube.allow_huge_operations = True
    mcube = cube.mask_out_bad_beams(0.1)
    mcube.beam_threshold = 1

    mx = mcube.max(axis=0)
    beam = mcube.beam if hasattr(mcube, 'beam') else mcube.average_beams(1)
    mx_K = (mx*u.beam).to(u.K, u.brightness_temperature(beam_area=beam,
                                                        disp=mcube.with_spectral_unit(u.GHz).spectral_axis.mean()))
    mx_K.write('collapse/max/{0}'.format(fn.replace(".image.pbcor.fits","_max_K.fits")),
               overwrite=True)
    mx_K.quicklook('collapse/max/pngs/{0}'.format(fn.replace(".image.pbcor.fits","_max_K.png")))


    mn = mcube.min(axis=0)
    beam = mcube.beam if hasattr(mcube, 'beam') else mcube.average_beams(1)
    mn_K = (mn*u.beam).to(u.K, u.brightness_temperature(beam_area=beam,
                                                        disp=mcube.with_spectral_unit(u.GHz).spectral_axis.mean()))
    mn_K.write('collapse/min/{0}'.format(fn.replace(".image.pbcor.fits","_min_K.fits")),
               overwrite=True)
    mn_K.quicklook('collapse/min/pngs/{0}'.format(fn.replace(".image.pbcor.fits","_min_K.png")))


    for pct in (25,50,75):
        pctmap = mcube.percentile(pct, axis=0)
        beam = mcube.beam if hasattr(mcube, 'beam') else mcube.average_beams(1)
        pctmap_K = (pctmap*u.beam).to(u.K,
                                      u.brightness_temperature(beam_area=beam,
                                                               disp=mcube.with_spectral_unit(u.GHz).spectral_axis.mean()))
        pctmap_K.write('collapse/percentile/{0}'.format(fn.replace(".image.pbcor.fits","_{0}pct_K.fits".format(pct))),
                       overwrite=True)
        pctmap_K.quicklook('collapse/percentile/pngs/{0}'.format(fn.replace(".image.pbcor.fits","_{0}pct_K.png".format(pct))))
