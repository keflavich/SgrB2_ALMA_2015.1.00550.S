
import numpy as np
import os
import glob
import datetime

def makefits(myimagebase):
    impbcor(imagename=myimagebase+'.image', pbimage=myimagebase+'.pb', outfile=myimagebase+'.image.pbcor', overwrite=True) # perform PBcorr
    exportfits(imagename=myimagebase+'.image.pbcor', fitsimage=myimagebase+'.image.pbcor.fits', dropdeg=True, overwrite=True) # export the corrected image
    exportfits(imagename=myimagebase+'.pb', fitsimage=myimagebase+'.pb.fits', dropdeg=True, overwrite=True) # export the PB image
    exportfits(imagename=myimagebase+'.model', fitsimage=myimagebase+'.model.fits', dropdeg=True, overwrite=True) # export the PB image
    exportfits(imagename=myimagebase+'.residual', fitsimage=myimagebase+'.residual.fits', dropdeg=True, overwrite=True) # export the PB image

if 'spwlist' not in locals():
    spwlist = ((0,25),(1,27),(2,29),(3,31))[::-1]
    print("Setting spwlist to {0}".format(spwlist))


mslist = ['uid___A002_Xc44eb5_X1139.ms.split.cal', 'uid___A002_Xc483da_Xa88.ms.split.cal']
print("MSes to be imaged are: {0}".format(mslist))

#for ms in mslist:
#    listobs(ms, listfile=ms+'.listobs', overwrite=True)

for spw,spw_orig in spwlist:

    for suffix, niter in (('clarkclean1000', 1000), ):
        
        step = 1920/32
        for startchan in np.arange(0, 1920, step):

            imagename = 'sgr_b2m.M.spw{0}.lines{2}-{3}.{1}'.format(spw, suffix, startchan, startchan+step)
            if not os.path.exists("{0}.image.pbcor.fits".format(imagename)):
                print("Imaging {0} at {1}".format(imagename, datetime.datetime.now()))
                tclean(vis=mslist,
                       imagename=imagename,
                       datacolumn='data',
                       spw=['{0}'.format(spw), '{0}'.format(spw)],
                       field=['5', '6'],
                       specmode='cube',
                       outframe='LSRK',
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
                       savemodel='none',
                       chanchunks=1,
                       interactive=False)
                makefits(imagename)
