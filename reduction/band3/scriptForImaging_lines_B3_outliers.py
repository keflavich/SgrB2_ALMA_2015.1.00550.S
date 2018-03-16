
import numpy as np
import os
import glob
import datetime
from scipy.fftpack import next_fast_len

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

for robust, imsize, cellsize in [(0.5, 5000, 0.007), (-2, 6000, 0.004)]:

    for spw,spw_orig in spwlist:

        for suffix, niter in (('clarkclean5000', 5000), ):

            imagename = 'sgr_b2m.spw{0}.B3.outlier.lines.{1}.robust{2}'.format(spw, suffix, robust,)

            if not os.path.exists("{0}.image.pbcor.fits".format(imagename)):
                print("Imaging {0} at {1}".format(imagename, datetime.datetime.now()))

                with open(imagename+'.outliers.txt','w') as fh:
                    for center, size, name in [
                                               #('ICRS 266.8327972d -28.37194822d', next_fast_len(int(8.0/cellsize)), 'N'), first non-outlier
                                               ('ICRS 266.8328864d -28.37045063d', next_fast_len(int(1.0/cellsize)), 'K7'),
                                               ('ICRS 266.8333160d -28.36797883d', next_fast_len(int(1.0/cellsize)), 'K4'),
                                               ('ICRS 266.8334869d -28.37814616d', next_fast_len(int(1.0/cellsize)), 'Z10.24'),
                                               ('ICRS 266.8340194d -28.38474960d', next_fast_len(int(12./cellsize)), 'M'),
                                               ('ICRS 266.8351475d -28.39588118d', next_fast_len(int(2.0/cellsize)), 'S'),
                                              ]:
                        fh.write("imagename={0}.{1}\n".format(imagename, name))
                        fh.write("imsize={0}\n".format(size))
                        fh.write("cell={0}arcsec\n".format(cellsize))
                        fh.write("phasecenter={0}\n".format(center))


                tclean(vis=mslist,
                       imagename=imagename+".N",
                       datacolumn='corrected',
                       phasecenter='ICRS 266.8327972d -28.37194822d',
                       spw=['{0}'.format(spw_orig), '{0}'.format(spw_orig)],
                       field=['5,6', '4,5'],
                       specmode='cube',
                       outframe='LSRK',
                       threshold='5mJy',
                       imsize=[imsize, imsize],
                       cell=['{0}arcsec'.format(cellsize)],
                       outlierfile=imagename+".outliers.txt",
                       niter=niter,
                       deconvolver='clark',
                       gridder='mosaic',
                       weighting='briggs',
                       robust=robust,
                       pbcor=True,
                       pblimit=0.2,
                       savemodel='none',
                       chanchunks=48,
                       parallel=True,
                       interactive=False)

                for suffix in ("N", "M", "K7", "K4", "Z10.24", "S"):
                    makefits(imagename+"."+suffix)
