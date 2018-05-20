import numpy as np
import turbustat.statistics.pca
from spectral_cube import SpectralCube
from turbustat.statistics.threeD_to_twoD import var_cov_cube


from astropy import constants, units as u, table, stats, coordinates, wcs, log, coordinates as coord, convolution, modeling, visualization
from astropy.io import fits

import paths


vcube = SpectralCube.read('/Volumes/external/sgrb2/full_SgrB2N_spw1_lines_cutoutN_medsub.fits')
cube = SpectralCube(data=vcube._data, wcs=vcube.wcs, mask=vcube.mask,
                    meta=vcube.meta, header=vcube.header,
                    beam=vcube.average_beams(threshold=0.1))

data = np.arcsinh(cube.filled_data[:].value)

cov_matrix = var_cov_cube(data, mean_sub=False)
all_eigsvals, eigvecs = np.linalg.eigh(cov_matrix)
all_eigsvals = np.real_if_close(all_eigsvals)
eigvecs = eigvecs[:, np.argsort(all_eigsvals)[::-1]]
all_eigsvals = np.sort(all_eigsvals)[::-1]

eigims = []
for ii in range(20):
    eigim = np.zeros(cube.shape[1:])
    for channel in range(cube.shape[0]):
        eigim += np.nan_to_num(data[channel] * np.real_if_close(eigvecs[channel, ii]))
    eigims.append(eigim)

hdul = fits.HDUList([fits.PrimaryHDU(np.array(eigims)),
                     fits.ImageHDU(cov_matrix),
                     fits.ImageHDU(all_eigsvals)
                    ])
hdul.writeto(paths.Fpath('eigenimages_SgrB2N_spw1.fits'), overwrite=True)


cov_matrix = var_cov_cube(data, mean_sub=True)
all_eigsvals, eigvecs = np.linalg.eigh(cov_matrix)
all_eigsvals = np.real_if_close(all_eigsvals)
eigvecs = eigvecs[:, np.argsort(all_eigsvals)[::-1]]
all_eigsvals = np.sort(all_eigsvals)[::-1]

eigims = []
for ii in range(20):
    eigim = np.zeros(cube.shape[1:])
    for channel in range(cube.shape[0]):
        mean_value = np.nanmean(data[channel])
        eigim += np.nan_to_num((data[channel] - mean_value) * np.real_if_close(eigvecs[channel, ii]))
    eigims.append(eigim)

hdul = fits.HDUList([fits.PrimaryHDU(np.array(eigims)),
                     fits.ImageHDU(cov_matrix),
                     fits.ImageHDU(all_eigsvals)
                    ])
hdul.writeto(paths.Fpath('eigenimages_SgrB2N_spw1_meansub.fits'), overwrite=True)
