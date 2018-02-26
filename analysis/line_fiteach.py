import numpy as np
import pyspeckit
import radio_beam
from astropy import units as u
from astropy import constants
from spectral_cube import SpectralCube

from line_frequencies import line_frequencies

cube = SpectralCube.read('sgr_b2m.N.spw0.lines.clarkclean1000.robust0.5.image.pbcor.fits').with_spectral_unit(u.GHz)


for freq in line_frequencies:
    dv = 10*u.km/u.s

    f1,f2 = (1-dv/constants.c) * freq, (1+dv/constants.c) * freq
    x1,x2 = np.argmin(np.abs(cube.spectral_axis-f1)), np.argmin(np.abs(cube.spectral_axis-f2))

    # universal mask
    mask = cube[x1:x2].max(axis=0) > 0.03*u.Jy/u.beam


    pcube = pyspeckit.Cube(cube=cube[x1:x2,:,:].convolve_to(radio_beam.Beam(0.08*u.arcsec, 0.08*u.arcsec)))

    pcube.cube -= pcube.cube.max(axis=0)

    sp = pcube.get_spectrum(545, 455)
    sp.specfit(guesses=[-0.001, freq.to(u.GHz).value, 3e6])

    pcube.fiteach(guesses=[-0.001, freq.to(u.GHz).value], maskmap=mask,
                  multicore=12, start_from_point=(545,455), signal_cut=0)

    pcube.write_fit('linefit_{0:0.3f}GHz.fits'.format(freq.to(u.GHz).value))
