import radio_beam
from astropy import units as u

# base dust opacity kappa271 from Aguirre 2011
kappa271 = 0.0114*u.cm**2/u.g

# average mass of an H2
mh2 = 2.8 * u.Da

# ALMA freq
almafreq = 96*u.GHz

# Bolocam freq
bolofreq = 271.1*u.GHz

# distance to sgrb2
d_sgrb2 = 8*u.kpc

beta = 2
ntau1_beta2 = (1/(kappa271 * (almafreq/bolofreq)**beta) / mh2).to(u.cm**-2)
beta = 1
ntau1_beta1 = (1/(kappa271 * (almafreq/bolofreq)**beta) / mh2).to(u.cm**-2)

print(f"column density at tau=1 for beta=2: {ntau1_beta2}")
print(f"column density at tau=1 for beta=1: {ntau1_beta1}")

beam = radio_beam.Beam(0.05*u.arcsec)

massperbeam_beta1 = (ntau1_beta1 * mh2 * (beam.sr * d_sgrb2**2)).to(u.M_sun, u.dimensionless_angles())
massperbeam_beta2 = (ntau1_beta2 * mh2 * (beam.sr * d_sgrb2**2)).to(u.M_sun, u.dimensionless_angles())

print(f"mass per beam at tau=1 for beta=2: {massperbeam_beta2}")
print(f"mass per beam at tau=1 for beta=1: {massperbeam_beta1}")
