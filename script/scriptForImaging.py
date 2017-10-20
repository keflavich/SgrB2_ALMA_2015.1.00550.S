import os
import glob

mslist = ['uid___A002_Xc44eb5_X1139.ms.split.cal', 'uid___A002_Xc483da_Xa88.ms.split.cal']

for ms in mslist:
    listobs(ms, listfile=ms+'.listobs')


# Image cube for source M in representative window:
tclean(vis=mslist,
       imagename='sgr_b2m.M.spw25',
       datacolumn='data',
       spw=['0', '0'],
       field=['4', '5'],
       specmode='cube', 
       width=1,
       start='',
       outframe='LSRK',
       nchan=-1,
       restfreq='217.10498GHz',
       threshold='1mJy', 
       imsize=[256, 256], 
       cell=['0.007arcsec'], 
       niter=1000, 
       deconvolver='multiscale', 
       gridder='standard', 
       weighting='briggs',
       robust=0.5,
       pbcor=True, 
       pblimit=0.2, 
       restoringbeam='common',
       chanchunks=-1, 
       interactive=True)

# Image cube for source N in representative window:
tclean(vis=mslist,
       imagename='sgr_b2m.N.spw25',
       datacolumn='data',
       spw=['0', '0'],
       field=['5', '6'],
       specmode='cube', 
       width=1,
       start='',
       outframe='LSRK',
       nchan=-1,
       restfreq='217.10498GHz',
       threshold='1mJy', 
       imsize=[256, 256], 
       cell=['0.007arcsec'], 
       niter=1000, 
       deconvolver='multiscale', 
       gridder='standard', 
       weighting='briggs',
       robust=0.5,
       pbcor=True, 
       pblimit=0.2, 
       restoringbeam='common',
       chanchunks=-1, 
       interactive=True)

#Subtract continuum
for ms in mslist:
    uvcontsub(vis = ms,
              field = 'sgr_b2m',
              fitspw = '0:0~60;97~146;183~344;467~505;552~585;667~820;854~907;967~1017;1134~1212;1250~1305;1653~1750;1820~1915',
              spw = '0',
              fitorder = 1,
              want_cont = True)

for ms in mslist:
    listobs(ms+'.contsub', listfile=ms+'.contsub.listobs')

mslistcsub = ['uid___A002_Xc44eb5_X1139.ms.split.cal.contsub', 'uid___A002_Xc483da_Xa88.ms.split.cal.contsub']

# Image cube for source M in representative window:
# Beam: 0.078"x0.040"
# RMS: 1.09 mJy/beam
tclean(vis=mslistcsub,
       imagename='sgr_b2m.M.spw25.nocont',
       datacolumn='data',
       spw='0',
       field='1',
       specmode='cube', 
       width=1,
       start='',
       outframe='LSRK',
       nchan=-1,
       restfreq='217.10498GHz',
       threshold='1mJy', 
       imsize=[256, 256], 
       cell=['0.007arcsec'], 
       niter=1000, 
       deconvolver='multiscale', 
       gridder='standard', 
       weighting='briggs',
       robust=0.5,
       pbcor=True, 
       pblimit=0.2, 
       restoringbeam='common',
       chanchunks=-1, 
       interactive=True)

# Image cube for source N in representative window:
# Beam: 0.078"x0.040"
# RMS: 1.36 mJy/beam
tclean(vis=mslistcsub,
       imagename='sgr_b2m.N.spw25.nocont',
       datacolumn='data',
       spw='0',
       field='2',
       specmode='cube', 
       width=1,
       start='',
       outframe='LSRK',
       nchan=-1,
       restfreq='217.10498GHz',
       threshold='1mJy', 
       imsize=[256, 256], 
       cell=['0.007arcsec'], 
       niter=1000, 
       deconvolver='multiscale', 
       gridder='standard', 
       weighting='briggs',
       robust=0.5,
       pbcor=True, 
       pblimit=0.2, 
       restoringbeam='common',
       chanchunks=-1, 
       interactive=True)

# # ## ## Apply a primary beam correction

myimages = glob.glob('*.image.pbcor')+glob.glob('*.pb')

for image in myimages:
    # Export the images to fits
    exportfits(imagename=image, fitsimage=image+'.fits', overwrite=True)
