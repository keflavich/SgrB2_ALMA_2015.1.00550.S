"""
Search for interesting HCN lines

Candidates are:
"""
import numpy as np
import paths
from astroquery.splatalogue import Splatalogue
from astropy import units as u
from spectral_cube import SpectralCube


lines = Splatalogue.query_lines(83*u.GHz, 103*u.GHz, chemical_name=' HCN ',
                                line_lists=['SLAIM'])
lines2 = Splatalogue.query_lines(214*u.GHz, 240*u.GHz, chemical_name=' HCN ',
                                 line_lists=['SLAIM'])
freq_key = lines.colnames[2]
qn_key = lines.colnames[6]
freqs = {row['Species']+"_"+row[qn_key]: row[freq_key]*u.GHz
         for row in lines}
freqs.update({row['Species']+"_"+row[qn_key]: row[freq_key]*u.GHz for
              row in lines2})


lines3 = Splatalogue.query_lines(83*u.GHz, 103*u.GHz, chemical_name=' HCO\+ ',
                                line_lists=['SLAIM'])
lines4 = Splatalogue.query_lines(214*u.GHz, 240*u.GHz, chemical_name=' HCO\+ ',
                                 line_lists=['SLAIM'])
freq_key = lines.colnames[2]
qn_key = lines.colnames[6]
freqs.update({row['Species']+"_"+row[qn_key]: row[freq_key]*u.GHz
              for row in lines3})
freqs.update({row['Species']+"_"+row[qn_key]: row[freq_key]*u.GHz for
              row in lines4})

print(freqs)


cubes = {}
mx = {}

for region in ("N","M"):
    for spw in (0,1,2,3):
        for band in (3,6):
            for line in freqs:
                fn = 'full_SgrB2{0}_spw{1}_lines_cutout{0}_medsub.fits'.format(region, spw)
                fn = 'sgr_b2m.{0}.spw{1}.B{2}.lines.clarkclean1000.robust0.5.image.pbcor.medsub.fits'.format(region, spw, band)
                cube = SpectralCube.read(paths.Fpath(fn))
                freq = freqs[line]
                if cube.spectral_extrema[0] < freq < cube.spectral_extrema[1]:
                    print("Matched {line} to spw {spw}".format(line=line, spw=spw))
                    subcube = (cube.with_spectral_unit(u.km/u.s,
                                                      velocity_convention='radio',
                                                      rest_value=freq)
                               .spectral_slab(25*u.km/u.s, 95*u.km/u.s)
                              )
                    try:
                        subcube = subcube.to(u.K)
                    except Exception as ex:
                        print("Failed: {0}".format(ex))
                    if 'OBJECT' in subcube.meta:
                        subcube.meta['OBJECT'] = subcube.meta['OBJECT'] + line
                    else:
                        subcube.meta['OBJECT'] = "{0}_{1}".format(region, line)
                    del subcube._header['OBJECT']
                    subcube._nowcs_header['OBJECT'] = subcube.meta['OBJECT']
                    subcube._header['OBJECT'] = subcube.meta['OBJECT']
                    cubes[(region,spw,line)] = subcube
                    mx[(region,spw,line)] = subcube.max(axis=0, how='slice')


import pyds9
dd = pyds9.DS9('hcnsgrb2')
#dd.set('lock frames wcs')
#dd.set('lock slice wcs')
for cubeid, cube in cubes.items():
    cube.to_ds9(ds9id=dd.id, newframe=True)

import pylab as pl
pl.close('all')
for name,mmm in mx.items():
    mmm.quicklook()

