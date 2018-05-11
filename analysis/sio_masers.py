"""
Search for the masers

Candidates are:
    SiO v=2 J=2-1 (North) 65-96 km/s
    29SiO v=0 J=2-1 (Main) 58-103 km/s
    SiO v=1 J=2-1 (Main) 58-103 km/s
    SiO v=0 J=2-1 (Main) 58-103 km/s
    SiO v=0 J=5-4 (Main) 58-103 km/s
"""
import numpy as np
import paths
from astroquery.splatalogue import Splatalogue
from astropy import units as u
from spectral_cube import SpectralCube


lines = Splatalogue.query_lines(83*u.GHz, 89*u.GHz, chemical_name='SiO',
                                line_lists=['SLAIM'])
lines2 = Splatalogue.query_lines(214*u.GHz, 220*u.GHz, chemical_name='SiO',
                                 line_lists=['SLAIM'])
freqs = {row['Species']+"_"+row['Resolved QNs']: row['Freq-GHz']*u.GHz
         for row in lines}
freqs.update({row['Species']+"_"+row['Resolved QNs']: row['Freq-GHz']*u.GHz for
              row in lines2})

maser_lines = ['SiOv=2_2-1', '29SiOv=0_2-1', 'SiOv=1_2-1', 'SiOv=0_2-1', 'SiOv=0_5-4']


cubes = {}
mx = {}
m1 = {}

for region in ("N","M"):
    for spw in (0,1,2,3):
        for band in (3,6):
            #for line in freqs:
            for line in maser_lines:
                fn = 'full_SgrB2{0}_spw{1}_lines_cutout{0}_medsub.fits'.format(region, spw)
                fn = 'sgr_b2m.{0}.spw{1}.B{2}.lines.clarkclean1000.robust0.5.image.pbcor.medsub.fits'.format(region, spw, band)
                cube = SpectralCube.read(paths.eFpath(fn))
                freq = freqs[line]
                if cube.spectral_extrema[0] < freq < cube.spectral_extrema[1]:
                    subcube = (cube.with_spectral_unit(u.km/u.s,
                                                      velocity_convention='radio',
                                                      rest_value=freq)
                               .spectral_slab(55*u.km/u.s, 110*u.km/u.s)
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
                    m1[(region,spw,line)] = subcube.moment1(axis=0)

