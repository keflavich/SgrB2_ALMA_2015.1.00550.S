import shutil
from astropy.io import fits
from spectral_cube import SpectralCube
from astropy import coordinates, units as u

centerN = coordinates.SkyCoord('17:47:19.877', '-28:22:18.39', frame='fk5', unit=(u.hour, u.deg))
centerM = coordinates.SkyCoord('17:47:20.166', '-28:23:04.68', frame='fk5', unit=(u.hour, u.deg))

for spw in (0,1,3,2):
    print("Extracting spw{0} M".format(spw))
    cube = SpectralCube.read('full_SgrB2M_spw{0}_lines.fits'.format(spw))
    center_M = centerM.transform_to(getattr(coordinates, cube.wcs.wcs.radesys))
    cx,cy = map(int, cube.wcs.celestial.wcs_world2pix(centerM.ra.deg, centerM.dec.deg, 0))
    cutout_M = cube[:, cy-250:cy+250, cx-250:cx+250]
    cutout_M.write("full_SgrB2M_spw{0}_lines_cutoutM.fits".format(spw), overwrite=True)

    print("Extracting spw{0} N".format(spw))
    cube = SpectralCube.read('full_SgrB2N_spw{0}_lines.fits'.format(spw))
    center_N = centerN.transform_to(getattr(coordinates, cube.wcs.wcs.radesys))
    cx,cy = map(int, cube.wcs.celestial.wcs_world2pix(centerN.ra.deg, centerN.dec.deg, 0))
    cutout_N = cube[:, cy-300:cy+300, cx-300:cx+300]
    cutout_N.write("full_SgrB2N_spw{0}_lines_cutoutN.fits".format(spw), overwrite=True)


def medsub(cube, fn, fn_medsub):
    med = cube.percentile(25,axis=0)

    shutil.copy(fn, fn_medsub)

    outfh = fits.open(fn_medsub, mode='update')

    for index,slice in enumerate(cube):
        outfh[0].data[index] = slice - med
        outfh.flush()

    outfh.flush()
    outfh.close()


for spw in (0,1,3,2):

    fn = 'full_SgrB2N_spw{0}_lines_cutoutN.fits'.format(spw)
    fn_medsub = 'full_SgrB2N_spw{0}_lines_cutoutN_medsub.fits'.format(spw)
    cube = SpectralCube.read(fn)
    cube = cube.mask_out_bad_beams(0.1)
    cube.beam_threshold = 0.11
    medsub(cube, fn, fn_medsub)

    fn = 'full_SgrB2M_spw{0}_lines_cutoutM.fits'.format(spw)
    fn_medsub = 'full_SgrB2M_spw{0}_lines_cutoutM_medsub.fits'.format(spw)
    cube = SpectralCube.read(fn)
    cube = cube.mask_out_bad_beams(0.1)
    cube.beam_threshold = 0.11
    medsub(cube, fn, fn_medsub)
