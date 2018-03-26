import numpy as np
from astropy.io import fits
from astropy import wcs
from astropy import visualization
from astropy import coordinates
from astropy import units as u

import reproject
import pylab as pl
import paths
import visualization_tools

def rgbfig(figfilename="SgrB2N_RGB.pdf",
           lims=[([266.83404223,  266.83172659]), ([-28.373138, -28.3698755])],
           scalebarx=coordinates.SkyCoord(266.833545*u.deg, -28.37283819*u.deg),
           redfn=paths.Fpath('SGRB2N-2012-Q.DePree_K.recentered.fits'),
           greenfn=paths.Fpath('sgr_b2m.N.B3.allspw.continuum.r0.5.clean1000.image.tt0.pbcor.fits'),
           bluefn=paths.Fpath('sgr_b2m.N.B6.allspw.continuum.r0.5.clean1000.image.tt0.pbcor.fits')):

    header = fits.getheader(redfn)
    celwcs = wcs.WCS(header).celestial

    redhdu = fits.open(redfn)
    greenhdu = fits.open(greenfn)
    bluehdu = fits.open(bluefn)

    greendata,_ = reproject.reproject_interp((greenhdu[0].data,
                                              wcs.WCS(greenhdu[0].header).celestial),
                                             celwcs,
                                             shape_out=redhdu[0].data.squeeze().shape)
    bluedata,_ = reproject.reproject_interp((bluehdu[0].data,
                                             wcs.WCS(bluehdu[0].header).celestial),
                                            celwcs,
                                            shape_out=redhdu[0].data.squeeze().shape)

    #def rescale(x):
    #    return (x-np.nanmin(x))/(np.nanmax(x) - np.nanmin(x))
    rescale = visualization.PercentileInterval(99.99)


    rgb = np.array([rescale(redhdu[0].data.squeeze()),
                    rescale(greendata),
                    rescale(bluedata),]).swapaxes(0,2).swapaxes(0,1)


    norm = visualization.ImageNormalize(rgb,
                                        interval=visualization.MinMaxInterval(),
                                        stretch=visualization.AsinhStretch())

    fig1 = pl.figure(1)
    fig1.clf()
    ax = fig1.add_subplot(1,1,1, projection=celwcs)
    pl.imshow(rgb, origin='lower', interpolation='none', norm=norm)

    (x1,x2),(y1,y2) = celwcs.wcs_world2pix(lims[0], lims[1], 0)
    ax.axis((x1,x2,y1,y2))

    visualization_tools.make_scalebar(ax, left_side=scalebarx,
                                      length=1.213*u.arcsec, label='0.05 pc')

    pl.savefig(paths.fpath(figfilename), bbox_inches='tight')

if __name__ == "__main__":

    rgbfig()

    rgbfig(figfilename='SgrB2M_RGB.pdf',
           lims=[(266.8350734, 266.832958), (-28.38600555, -28.3832)],
           redfn=paths.Fpath('SGRB2M-2012-Q-MEAN.DePree.recentered.fits'),
           greenfn=paths.Fpath('sgr_b2m.M.B3.allspw.continuum.r0.5.clean1000.image.tt0.pbcor.fits'),
           bluefn=paths.Fpath('sgr_b2m.M.B6.allspw.continuum.r0.5.clean1000.image.tt0.pbcor.fits'),
           scalebarx=coordinates.SkyCoord(266.8336007*u.deg, -28.38553839*u.deg),
          )
