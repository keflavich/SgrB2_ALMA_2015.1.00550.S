import numpy as np
import reproject
from astropy.io import fits
from astropy import wcs
import image_registration

depree_m = fits.open('SGRB2M-2012-Q-MEAN.DePree.fits')
alma_m = fits.open('sgr_b2m.M.B3.allspw.continuum.r0.5.clean1000.image.tt0.pbcor.fits')

depree_m_fix = fits.PrimaryHDU(depree_m[0].data.squeeze(), wcs.WCS(depree_m[0].header).celestial.to_header())
alma_m_fix = fits.PrimaryHDU(alma_m[0].data.squeeze(), wcs.WCS(alma_m[0].header).celestial.to_header())

alma_reproj,_ = reproject.reproject_interp(alma_m_fix, depree_m_fix.header)
alma_ref = fits.PrimaryHDU(alma_reproj/np.nanmax(alma_reproj), depree_m_fix.header)
depree_m_fix = fits.PrimaryHDU(depree_m[0].data.squeeze()/np.nanmax(depree_m[0].data), wcs.WCS(depree_m[0].header).celestial.to_header())

dx,dy,dxw,dyw,edx,edy,edxw,edyw, proj1, proj2, shift, hdr =\
        image_registration.FITS_tools.match_images.register_fits(alma_ref,
                                                                 depree_m_fix,
                                                                 verbose=True,
                                                                 return_shifted_image=True,
                                                                 return_header=True,
                                                                 return_cropped_images=True,
                                                                 zeromean=True,
                                                                 boundary='constant',
                                                                 mindiff=0.001)
depree_m_shifted = fits.PrimaryHDU(shift, hdr)
depree_m_shifted.writeto('SGRB2M-2012-Q-MEAN.DePree.registeredALMAB3.fits', overwrite=True)



depree_n = fits.open('SGRB2N-2012-Q.DePree.fits')
alma_n = fits.open('sgr_b2m.N.B3.allspw.continuum.r0.5.clean1000.image.tt0.pbcor.fits')

depree_n_fix = fits.PrimaryHDU(depree_n[0].data.squeeze(), wcs.WCS(depree_n[0].header).celestial.to_header())
alma_n_fix = fits.PrimaryHDU(alma_n[0].data.squeeze(), wcs.WCS(alma_n[0].header).celestial.to_header())

alma_reproj,_ = reproject.reproject_interp(alma_n_fix, depree_n_fix.header)
alma_ref = fits.PrimaryHDU(alma_reproj/np.nanmax(alma_reproj), depree_n_fix.header)
depree_n_fix = fits.PrimaryHDU(depree_n[0].data.squeeze()/np.nanmax(depree_n[0].data), wcs.WCS(depree_n[0].header).celestial.to_header())

dx,dy,dxw,dyw,edx,edy,edxw,edyw, proj1, proj2, shift, hdr =\
        image_registration.FITS_tools.match_images.register_fits(alma_ref,
                                                                 depree_n_fix,
                                                                 verbose=True,
                                                                 return_shifted_image=True,
                                                                 return_header=True,
                                                                 return_cropped_images=True,
                                                                 zeromean=True,
                                                                 boundary='constant',
                                                                 mindiff=0.001)

depree_n_shifted = fits.PrimaryHDU(shift, hdr)
depree_n_shifted.writeto('SGRB2N-2012-Q.DePree.registeredALMAB3.fits', overwrite=True)
