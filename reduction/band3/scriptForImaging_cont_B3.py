
import datetime
import os
import glob

def makefits(myimagebase, cleanup=True):
    impbcor(imagename=myimagebase+'.image.tt0', pbimage=myimagebase+'.pb.tt0', outfile=myimagebase+'.image.tt0.pbcor', overwrite=True) # perform PBcorr
    exportfits(imagename=myimagebase+'.image.tt0.pbcor', fitsimage=myimagebase+'.image.tt0.pbcor.fits', dropdeg=True, overwrite=True) # export the corrected image
    exportfits(imagename=myimagebase+'.image.tt1', fitsimage=myimagebase+'.image.tt1.fits', dropdeg=True, overwrite=True) # export the corrected image
    exportfits(imagename=myimagebase+'.pb.tt0', fitsimage=myimagebase+'.pb.tt0.fits', dropdeg=True, overwrite=True) # export the PB image
    exportfits(imagename=myimagebase+'.model.tt0', fitsimage=myimagebase+'.model.tt0.fits', dropdeg=True, overwrite=True) # export the PB image
    exportfits(imagename=myimagebase+'.model.tt1', fitsimage=myimagebase+'.model.tt1.fits', dropdeg=True, overwrite=True) # export the PB image
    exportfits(imagename=myimagebase+'.residual.tt0', fitsimage=myimagebase+'.residual.tt0.fits', dropdeg=True, overwrite=True) # export the PB image
    exportfits(imagename=myimagebase+'.alpha', fitsimage=myimagebase+'.alpha.fits', dropdeg=True, overwrite=True)
    exportfits(imagename=myimagebase+'.alpha.error', fitsimage=myimagebase+'.alpha.error.fits', dropdeg=True, overwrite=True)

    if cleanup:
        for ttsuffix in ('.tt0', '.tt1', 'tt2'):
            for suffix in ('pb{tt}', 'weight', 'sumwt{tt}', 'psf{tt}',
                           'model{tt}', 'mask', 'image{tt}', 'residual{tt}',
                           'alpha', ):
                os.system('rm -rf {0}.{1}'.format(myimagebase, suffix).format(tt=ttsuffix))




mslist = ['uid___A002_Xc49eba_X108.ms', 'uid___A002_Xc49eba_X5a8.ms']

#for ms in mslist:
#    listobs(ms, listfile=ms+'.listobs')

source_spws = (25,27,29,31)

spwtext = ",".join(str(x) for x in source_spws)
for suffix, niter in (('dirty', 0), ('clean1000', 1000), ):

    for robust in (0.5, -2):

        imagename = 'sgr_b2m.M.B3.allspw.continuum.r{1}.{0}'.format(suffix, robust)
        if not os.path.exists("{0}.image.tt0.pbcor.fits".format(imagename)):
            print("Imaging {0} at {1}".format(imagename, datetime.datetime.now()))
            tclean(vis=mslist,
                   imagename=imagename,
                   datacolumn='corrected',
                   spw=[spwtext, spwtext],
                   field=['5', '4'],
                   specmode='mfs',
                   start='',
                   outframe='LSRK',
                   threshold='1mJy',
                   imsize=[6000, 6000],
                   cell=['0.007arcsec'],
                   niter=niter,
                   deconvolver='mtmfs',
                   nterms=2,
                   gridder='standard',
                   weighting='briggs',
                   robust=robust,
                   pbcor=True,
                   pblimit=0.2,
                   interactive=False)
            makefits(imagename)

        imagename = 'sgr_b2m.N.B3.allspw.continuum.r{1}.{0}'.format(suffix, robust)
        if not os.path.exists("{0}.image.tt0.pbcor.fits".format(imagename)):
            print("Imaging {0} at {1}".format(imagename, datetime.datetime.now()))
            tclean(vis=mslist,
                   imagename=imagename,
                   datacolumn='corrected',
                   spw=[spwtext, spwtext],
                   field=['6', '5'],
                   specmode='mfs',
                   start='',
                   outframe='LSRK',
                   threshold='1mJy',
                   imsize=[6000, 6000],
                   cell=['0.007arcsec'],
                   niter=niter,
                   deconvolver='mtmfs',
                   nterms=2,
                   gridder='standard',
                   weighting='briggs',
                   robust=robust,
                   pbcor=True,
                   pblimit=0.2,
                   interactive=False)
            makefits(imagename)




for spw,spw_orig in enumerate(source_spws):

    for suffix, niter in (('dirty', 0), ('clean1000', 1000), ):

        for robust in (0.5, -2):

            imagename = 'sgr_b2m.M.B3.spw{0}.continuum.r{2}.{1}'.format(spw, suffix, robust)
            if not os.path.exists("{0}.image.tt0.pbcor.fits".format(imagename)):
                print("Imaging {0} at {1}".format(imagename, datetime.datetime.now()))
                tclean(vis=mslist,
                       imagename=imagename,
                       datacolumn='corrected',
                       spw=['{0}'.format(spw_orig), '{0}'.format(spw_orig)],
                       field=['5', '4'],
                       specmode='mfs',
                       start='',
                       outframe='LSRK',
                       threshold='1mJy',
                       imsize=[6000, 6000],
                       cell=['0.007arcsec'],
                       niter=niter,
                       deconvolver='mtmfs',
                       nterms=2,
                       gridder='standard',
                       weighting='briggs',
                       robust=0.5,
                       pbcor=True,
                       pblimit=0.2,
                       interactive=False)
                makefits(imagename)

            imagename = 'sgr_b2m.N.B3.spw{0}.continuum.r{2}.{1}'.format(spw, suffix, robust)
            if not os.path.exists("{0}.image.tt0.pbcor.fits".format(imagename)):
                print("Imaging {0} at {1}".format(imagename, datetime.datetime.now()))
                tclean(vis=mslist,
                       imagename=imagename,
                       datacolumn='corrected',
                       spw=['{0}'.format(spw_orig), '{0}'.format(spw_orig)],
                       field=['6', '5'],
                       specmode='mfs',
                       start='',
                       outframe='LSRK',
                       threshold='1mJy',
                       imsize=[6000, 6000],
                       cell=['0.007arcsec'],
                       niter=niter,
                       deconvolver='mtmfs',
                       nterms=2,
                       gridder='standard',
                       weighting='briggs',
                       robust=0.5,
                       pbcor=True,
                       pblimit=0.2,
                       interactive=False)
                makefits(imagename)

## these all have wrong SPWs
# suffix='clean1000'
# niter=1000
# imagename = 'sgr_b2m.M.B3.allspw.continuum.r0.5.{0}'.format(spw, suffix)
# tclean(vis=mslist,
#        imagename=imagename,
#        datacolumn='corrected',
#        spw=['0,1,2,3', '0,1,2,3'],
#        field=['4', '5'],
#        specmode='mfs',
#        start='',
#        outframe='LSRK',
#        nchan=-1,
#        threshold='1mJy',
#        imsize=[6000, 6000],
#        cell=['0.007arcsec'],
#        niter=niter,
#        deconvolver='mtmfs',
#        gridder='standard',
#        weighting='briggs',
#        robust=0.5,
#        pbcor=True,
#        pblimit=0.2,
#        interactive=False)
# makefits(imagename)
# 
# imagename = 'sgr_b2m.N.B3.allspw.continuum.r0.5.{0}'.format(suffix)
# tclean(vis=mslist,
#        imagename=imagename,
#        datacolumn='corrected',
#        spw=['0,1,2,3', '0,1,2,3'],
#        field=['5', '6'],
#        specmode='mfs',
#        start='',
#        outframe='LSRK',
#        nchan=-1,
#        threshold='1mJy',
#        imsize=[6000, 6000],
#        cell=['0.007arcsec'],
#        niter=niter,
#        deconvolver='mtmfs',
#        gridder='standard',
#        weighting='briggs',
#        robust=0.5,
#        pbcor=True,
#        pblimit=0.2,
#        interactive=False)
# makefits(imagename)
# 
# 
# 
# 
# 
# suffix='r-2.cleanto5mJy_2terms'
# niter=100000
# imagename = 'sgr_b2m.M.B3.allspw.continuum.{0}'.format(suffix)
# tclean(vis=mslist,
#        imagename=imagename,
#        datacolumn='corrected',
#        spw=['0,1,2,3', '0,1,2,3'],
#        field=['4', '5'],
#        specmode='mfs',
#        deconvolver='mtmfs',
#        nterms=2,
#        scales=[0,4,12],
#        outframe='LSRK',
#        threshold='5mJy',
#        imsize=[6000, 6000],
#        cell=['0.007arcsec'],
#        niter=niter,
#        gridder='standard',
#        weighting='briggs',
#        robust=-2,
#        pbcor=True,
#        pblimit=0.2,
#        interactive=False)
# makefits(imagename)
# 
# imagename = 'sgr_b2m.N.B3.allspw.continuum.{0}'.format(suffix)
# tclean(vis=mslist,
#        imagename=imagename,
#        datacolumn='corrected',
#        spw=['0,1,2,3', '0,1,2,3'],
#        field=['5', '6'],
#        specmode='mfs',
#        deconvolver='mtmfs',
#        nterms=2,
#        scales=[0,4,12],
#        outframe='LSRK',
#        threshold='5mJy',
#        imsize=[6000, 6000],
#        cell=['0.007arcsec'],
#        niter=niter,
#        gridder='standard',
#        weighting='briggs',
#        robust=-2,
#        pbcor=True,
#        pblimit=0.2,
#        interactive=False)
# makefits(imagename)
