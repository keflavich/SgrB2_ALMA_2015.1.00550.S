
import numpy as np
import os
import glob
import datetime

def makefits(myimagebase, cleanup=True):
    impbcor(imagename=myimagebase+'.image', pbimage=myimagebase+'.pb', outfile=myimagebase+'.image.pbcor', overwrite=True) # perform PBcorr
    exportfits(imagename=myimagebase+'.image.pbcor', fitsimage=myimagebase+'.image.pbcor.fits', dropdeg=True, overwrite=True) # export the corrected image
    exportfits(imagename=myimagebase+'.pb', fitsimage=myimagebase+'.pb.fits', dropdeg=True, overwrite=True) # export the PB image
    exportfits(imagename=myimagebase+'.model', fitsimage=myimagebase+'.model.fits', dropdeg=True, overwrite=True) # export the PB image
    exportfits(imagename=myimagebase+'.residual', fitsimage=myimagebase+'.residual.fits', dropdeg=True, overwrite=True) # export the PB image

    if cleanup:
        for suffix in ('psf', 'weight', 'sumwt', 'pb', 'model', 'residual',
                       'mask', 'image'):
            os.system('rm -rf {0}.{1}'.format(myimagebase, suffix))


if 'spwlist' not in locals():
    spwlist = ((0,25),(1,27),(2,29),(3,31))[::-1]
    print("Setting spwlist to {0}".format(spwlist))



mslist = ['uid___A002_Xc44eb5_X1139.ms.split.cal', 'uid___A002_Xc483da_Xa88.ms.split.cal']

for ms in mslist:
    listobs(ms, listfile=ms+'.listobs', overwrite=True)

for spw,spw_orig in spwlist:

    for suffix, niter in (('clarkclean1000', 1000), ):
        
        for robust, imsize, cellsize in [(0.5, 1000, 0.007), (-2, 1750, 0.004)]:

            imagename = 'sgr_b2m.N.spw{0}.lines.{1}.robust{2}'.format(spw, suffix, robust)
            if not os.path.exists("{0}.image.pbcor.fits".format(imagename)):
                print("Imaging {0} at {1}".format(imagename, datetime.datetime.now()))
                tclean(vis=mslist,
                       imagename=imagename,
                       datacolumn='data',
                       phasecenter='ICRS 17:47:19.878s -28.22.18.549',
                       spw=['{0}'.format(spw), '{0}'.format(spw)],
                       field=['5', '6'],
                       specmode='cube',
                       outframe='LSRK',
                       threshold='1mJy',
                       imsize=[imsize, imsize],
                       cell=['{0}arcsec'.format(cellsize)],
                       niter=niter,
                       deconvolver='clark',
                       gridder='standard',
                       weighting='briggs',
                       robust=robust,
                       pbcor=True,
                       pblimit=0.2,
                       savemodel='none',
                       parallel=True,
                       interactive=False)
                makefits(imagename)


# do M second
for spw,spw_orig in spwlist:

    for suffix, niter in (('clarkclean1000', 1000), ):
        
        for robust, imsize, cellsize in [(0.5, 1000, 0.007), (-2, 1750, 0.004)]:

            imagename = 'sgr_b2m.M.spw{0}.lines{1}.robust{2}'.format(spw, suffix, robust)
            if not os.path.exists("{0}.image.pbcor.fits".format(imagename)):
                print("Imaging {0} at {1}".format(imagename, datetime.datetime.now()))
                tclean(vis=mslist,
                       imagename=imagename,
                       datacolumn='data',
                       spw=['{0}'.format(spw), '{0}'.format(spw)],
                       field=['4', '5'],
                       specmode='cube',
                       outframe='LSRK',
                       threshold='10mJy',
                       imsize=[imsize, imsize],
                       cell=['{0}arcsec'.format(cellsize)],
                       niter=niter,
                       deconvolver='clark',
                       gridder='standard',
                       weighting='briggs',
                       robust=robust,
                       phasecenter='ICRS 17:47:20.161 -28.23.04.624',
                       pbcor=True,
                       pblimit=0.2,
                       savemodel='none',
                       parallel=True,
                       interactive=False)
                makefits(imagename)
