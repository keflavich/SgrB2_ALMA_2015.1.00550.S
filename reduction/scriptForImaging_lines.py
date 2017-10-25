
import os
import glob

def makefits(myimagebase):
    impbcor(imagename=myimagebase+'.image', pbimage=myimagebase+'.pb', outfile=myimagebase+'.image.pbcor', overwrite=True) # perform PBcorr
    exportfits(imagename=myimagebase+'.image.pbcor', fitsimage=myimagebase+'.image.pbcor.fits', dropdeg=True, overwrite=True) # export the corrected image
    exportfits(imagename=myimagebase+'.pb', fitsimage=myimagebase+'.pb.fits', dropdeg=True, overwrite=True) # export the PB image
    exportfits(imagename=myimagebase+'.model', fitsimage=myimagebase+'.model.fits', dropdeg=True, overwrite=True) # export the PB image
    exportfits(imagename=myimagebase+'.residual', fitsimage=myimagebase+'.residual.fits', dropdeg=True, overwrite=True) # export the PB image



mslist = ['uid___A002_Xc44eb5_X1139.ms.split.cal', 'uid___A002_Xc483da_Xa88.ms.split.cal']

for ms in mslist:
    listobs(ms, listfile=ms+'.listobs')

for spw,spw_orig in enumerate((25,27,29,31)):

    for suffix, niter in (('dirty', 0), ('clarkclean1000', 1000), ):

        imagename = 'sgr_b2m.M.spw{0}.lines.{1}'.format(spw, suffix)
        tclean(vis=mslist,
               imagename=imagename,
               datacolumn='data',
               spw=['{0}'.format(spw), '{0}'.format(spw)],
               field=['4', '5'],
               specmode='cube',
               start='',
               outframe='LSRK',
               nchan=-1,
               threshold='10mJy',
               imsize=[6000, 6000],
               cell=['0.007arcsec'],
               niter=niter,
               deconvolver='clark',
               gridder='standard',
               weighting='briggs',
               robust=0.5,
               pbcor=True,
               pblimit=0.2,
               interactive=False)
        makefits(imagename)

        imagename = 'sgr_b2m.N.spw{0}.lines.{1}'.format(spw, suffix)
        tclean(vis=mslist,
               imagename=imagename,
               datacolumn='data',
               spw=['{0}'.format(spw), '{0}'.format(spw)],
               field=['5', '6'],
               specmode='cube',
               start='',
               outframe='LSRK',
               nchan=-1,
               threshold='1mJy',
               imsize=[6000, 6000],
               cell=['0.007arcsec'],
               niter=niter,
               deconvolver='clark',
               gridder='standard',
               weighting='briggs',
               robust=0.5,
               pbcor=True,
               pblimit=0.2,
               interactive=False)
        makefits(imagename)
