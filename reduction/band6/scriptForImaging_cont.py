
import os
import glob

def makefits(myimagebase):
    impbcor(imagename=myimagebase+'.image.tt0', pbimage=myimagebase+'.pb.tt0', outfile=myimagebase+'.image.tt0.pbcor', overwrite=True) # perform PBcorr
    exportfits(imagename=myimagebase+'.image.tt0.pbcor', fitsimage=myimagebase+'.image.tt0.pbcor.fits', dropdeg=True, overwrite=True) # export the corrected image
    exportfits(imagename=myimagebase+'.image.tt1', fitsimage=myimagebase+'.image.tt1.fits', dropdeg=True, overwrite=True) # export the corrected image
    exportfits(imagename=myimagebase+'.pb.tt0', fitsimage=myimagebase+'.pb.tt0.fits', dropdeg=True, overwrite=True) # export the PB image
    exportfits(imagename=myimagebase+'.model.tt0', fitsimage=myimagebase+'.model.tt0.fits', dropdeg=True, overwrite=True) # export the PB image
    exportfits(imagename=myimagebase+'.model.tt1', fitsimage=myimagebase+'.model.tt1.fits', dropdeg=True, overwrite=True) # export the PB image
    exportfits(imagename=myimagebase+'.residual.tt0', fitsimage=myimagebase+'.residual.tt0.fits', dropdeg=True, overwrite=True) # export the PB image
    exportfits(imagename=myimagebase+'.alpha', fitsimage=myimagebase+'.alpha.fits', dropdeg=True, overwrite=True)
    exportfits(imagename=myimagebase+'.alpha.error', fitsimage=myimagebase+'.alpha.error.fits', dropdeg=True, overwrite=True)



mslist = ['uid___A002_Xc44eb5_X1139.ms.split.cal', 'uid___A002_Xc483da_Xa88.ms.split.cal']

for ms in mslist:
    listobs(ms, listfile=ms+'.listobs')

for spw,spw_orig in enumerate((25,27,29,31)):

    for suffix, niter in (('dirty', 0), ('clean1000', 1000), ):

        imagename = 'sgr_b2m.M.spw{0}.continuum.{1}'.format(spw, suffix)
        tclean(vis=mslist,
               imagename=imagename,
               datacolumn='data',
               spw=['{0}'.format(spw), '{0}'.format(spw)],
               field=['4', '5'],
               specmode='mfs',
               start='',
               outframe='LSRK',
               nchan=-1,
               restfreq='217.10498GHz',
               threshold='1mJy',
               imsize=[6000, 6000],
               cell=['0.007arcsec'],
               niter=niter,
               deconvolver='mtmfs',
               gridder='standard',
               weighting='briggs',
               robust=0.5,
               pbcor=True,
               pblimit=0.2,
               interactive=False)
        makefits(imagename)

        imagename = 'sgr_b2m.N.spw{0}.continuum.{1}'.format(spw, suffix)
        tclean(vis=mslist,
               imagename=imagename,
               datacolumn='data',
               spw=['{0}'.format(spw), '{0}'.format(spw)],
               field=['5', '6'],
               specmode='mfs',
               start='',
               outframe='LSRK',
               nchan=-1,
               restfreq='217.10498GHz',
               threshold='1mJy',
               imsize=[6000, 6000],
               cell=['0.007arcsec'],
               niter=niter,
               deconvolver='mtmfs',
               gridder='standard',
               weighting='briggs',
               robust=0.5,
               pbcor=True,
               pblimit=0.2,
               interactive=False)
        makefits(imagename)

suffix='clean1000'
niter=1000
imagename = 'sgr_b2m.M.allspw.continuum.{0}'.format(spw, suffix)
tclean(vis=mslist,
       imagename=imagename,
       datacolumn='data',
       spw=['0,1,2,3', '0,1,2,3'],
       field=['4', '5'],
       specmode='mfs',
       start='',
       outframe='LSRK',
       nchan=-1,
       threshold='1mJy',
       imsize=[6000, 6000],
       cell=['0.007arcsec'],
       niter=niter,
       deconvolver='mtmfs',
       gridder='standard',
       weighting='briggs',
       robust=0.5,
       pbcor=True,
       pblimit=0.2,
       interactive=False)
makefits(imagename)

imagename = 'sgr_b2m.N.allspw.continuum.{0}'.format(suffix)
tclean(vis=mslist,
       imagename=imagename,
       datacolumn='data',
       spw=['0,1,2,3', '0,1,2,3'],
       field=['5', '6'],
       specmode='mfs',
       start='',
       outframe='LSRK',
       nchan=-1,
       threshold='1mJy',
       imsize=[6000, 6000],
       cell=['0.007arcsec'],
       niter=niter,
       deconvolver='mtmfs',
       gridder='standard',
       weighting='briggs',
       robust=0.5,
       pbcor=True,
       pblimit=0.2,
       interactive=False)
makefits(imagename)
