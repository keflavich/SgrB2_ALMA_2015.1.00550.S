from spectral_cube import SpectralCube
from astropy import log
import os

for spw in (0,1,2,3):
    for band, percentile in ((3,50), (6,15)):
        """
        I had to experiment with several percentiles.
        90th percentile is probably the emission line ceiling
        50th percentile is halfway between emission and absorption and is therefore useless
        sigma clipping is pretty bad too
        15th percentile picks out some really awful spatial artifacts
        """
        for source in 'NM':

            basefn = 'sgr_b2m.{source}.spw{spw}.B{band}.lines.clarkclean1000.robust0.5.image.pbcor'.format(**locals())
            fn = basefn+".fits"
            if not os.path.exists(fn):
                log.warning("{0} does not exist".format(fn))
                continue
            outfn = basefn+".medsub.fits"
            outcontfn = basefn+".cont.fits"
            if not os.path.exists(outfn):

                log.info("Continuum subtracting at {0}% {1}->{2}".format(percentile, basefn, outfn))
                cube = SpectralCube.read(fn)
                cont = cube.mask_out_bad_beams(threshold=0.1).percentile(percentile, axis=0)
                cube.allow_huge_operations = True

                cont.write(outcontfn, overwrite=True)

                cscube = cube - cont
                cscube.write(outfn)
