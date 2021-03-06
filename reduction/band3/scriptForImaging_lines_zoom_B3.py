
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
    spwlist = ((0,25),(1,27),(2,29),(3,31))
    print("Setting spwlist to {0}".format(spwlist))



mslist = ['uid___A002_Xc49eba_X108.ms', 'uid___A002_Xc49eba_X5a8.ms']

# # check that things are sane....
# tb.open(mslist[0])
# corr = tb.getcol('CORRECTED_DATA', nrow=10)
# uncorr = tb.getcol('DATA', nrow=10)
# assert not np.any(corr == uncorr)
# tb.close()
# 
# ms.open(mslist[0])
# ms.msselect({'field':'sgr_b2m', 'spw':'29', 'antenna':'0'})
# didn't downselect enough; this takes a long time
# data = ms.getdata(['amplitude', 'corrected_amplitude', 'phase', 'corrected_phase'])
# ms.close()


#for ms in mslist:
#    listobs(ms, listfile=ms+'.listobs', overwrite=True)

for robust, imsize, cellsize in [(0.5, 1000, 0.007), (-2, 1200, 0.004)]:

    for spw,spw_orig in spwlist:

        for suffix, niter in (('clarkclean1000', 1000), ):

            imagename = 'sgr_b2m.N.spw{0}.B3.lines.{1}.robust{2}'.format(spw, suffix, robust)
            if not os.path.exists("{0}.image.pbcor.fits".format(imagename)):
                print("Imaging {0} at {1}".format(imagename, datetime.datetime.now()))
                tclean(vis=mslist,
                       imagename=imagename,
                       datacolumn='corrected',
                       phasecenter='ICRS 17:47:19.878 -28.22.18.549',
                       spw=['{0}'.format(spw_orig), '{0}'.format(spw_orig)],
                       field=['6', '5'],
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
                       parallel=False,
                       interactive=False)
                makefits(imagename)


# do M second
for robust, imsize, cellsize in [(0.5, 1000, 0.007), (-2, 1200, 0.004)]:

    for spw,spw_orig in spwlist:

        for suffix, niter in (('clarkclean1000', 1000), ):

            imagename = 'sgr_b2m.M.spw{0}.B3.lines.{1}.robust{2}'.format(spw, suffix, robust)
            if not os.path.exists("{0}.image.pbcor.fits".format(imagename)):
                print("Imaging {0} at {1}".format(imagename, datetime.datetime.now()))
                tclean(vis=mslist,
                       imagename=imagename,
                       datacolumn='corrected',
                       spw=['{0}'.format(spw_orig), '{0}'.format(spw_orig)],
                       field=['5', '4'],
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
                       parallel=False,
                       interactive=False)
                makefits(imagename)
