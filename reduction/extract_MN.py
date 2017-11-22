from spectral_cube import SpectralCube

for spw in (0,1,2,3):
    cube = SpectralCube.read('full_SgrB2M_spw{0}_lines.fits'.format(spw))
    cutout_M = cube[:, 2850-250:2850+250, 2850-250:2850+250]
    cutout_M.write("full_SgrB2M_spw0_lines_cutoutM.fits", overwrite=True)

    cube = SpectralCube.read('full_SgrB2N_spw{0}_lines.fits'.format(spw))
    cutout_N = cube[:, 2500:3200, 2600:3200]
    cutout_N.write("full_SgrB2N_spw0_lines_cutoutN.fits", overwrite=True)
