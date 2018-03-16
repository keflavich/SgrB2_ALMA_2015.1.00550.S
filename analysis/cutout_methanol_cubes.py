from spectral_cube import SpectralCube
from astropy import units as u
from astropy import log
from astroquery.splatalogue import Splatalogue
import os
import pylab as pl

pl.ioff()

for spw in (0,1,2,3):
    for band in (3,6):
        for source in 'NM':

            basefn = 'sgr_b2m.{source}.spw{spw}.B{band}.lines.clarkclean1000.robust0.5.image.pbcor.medsub'.format(**locals())
            fn = basefn+".fits"
            if not os.path.exists(fn):
                log.warning("{0} does not exist".format(fn))
                continue

            cube = SpectralCube.read(fn)

            lines = Splatalogue.query_lines(cube.spectral_axis.min(),
                                            cube.spectral_axis.max(),
                                            line_lists=['SLAIM'],
                                            chemical_name=' CH3OH',
                                           )

            print(lines)

            for row in lines:
                freq = row['Freq-GHz'] * u.GHz
                qn = row['Resolved QNs']
                species = row['Species']
                name = ('{1}_{0}'.format(qn, species)
                        .replace('(-','(m')
                        .replace(',-',',m')
                        .replace('-','_')
                        .replace('(','')
                        .replace(')','')
                        .replace(',','')
                       )


                outfn = basefn+".{0}.fits".format(name)
                if not os.path.exists(outfn):

                    ch3oh = (cube.with_spectral_unit(u.km/u.s, rest_value=freq,
                                                     velocity_convention='radio')
                             .spectral_slab(50*u.km/u.s, 75*u.km/u.s)
                            )
                    if hasattr(cube, 'mask_out_bad_beams'):
                        ch3oh = ch3oh.mask_out_bad_beams(threshold=0.1)
                    if ch3oh.shape[0] < 10:
                        log.warning("{0} is not really in range".format(name))
                        continue
                    ch3oh.write(outfn)

                    m0 = ch3oh.moment0()
                    m0.write('collapse/ch3oh/{0}_{1:0.2f}GHz_m0.fits'.format(name, freq.value), overwrite=True)

                    pl.figure(1)
                    pl.clf()
                    m0.quicklook('collapse/ch3oh/pngs/{0}_{1:0.2f}GHz_m0.png'.format(name, freq.value))

                    m1 = ch3oh.moment1()
                    m1.write('collapse/ch3oh/{0}_{1:0.2f}GHz_m1.fits'.format(name, freq.value), overwrite=True)

                    pl.figure(1)
                    pl.clf()
                    m1.quicklook('collapse/ch3oh/pngs/{0}_{1:0.2f}GHz_m1.png'.format(name, freq.value))

                    mx = ch3oh.max(axis=0)
                    mx.write('collapse/ch3oh/{0}_{1:0.2f}GHz_max.fits'.format(name, freq.value), overwrite=True)

                    pl.figure(1)
                    pl.clf()
                    mx.quicklook('collapse/ch3oh/pngs/{0}_{1:0.2f}GHz_max.png'.format(name, freq.value))

                    pl.close('all')
