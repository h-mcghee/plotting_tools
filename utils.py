import numpy as np

def idx(x, value):
    return np.argmin(np.abs(x - value))

def tof2energy(x, hv, s, t0, E0):
    """
    function for converting from TOF to energy
    requires:
    t the time of flight
    parameters:
        hv - photon energy
        s - source to detector distance
        t0 - start time
        E0 - potential offset in source
    """
    Me = 9.1093897e-31  # mass electron in kg
    ES = 6.242e18  # electrons per s

    eKE = (ES * 0.5 * Me) * ((1e9 * s / (x - t0))**2)  - E0

    BE = hv - eKE
    return BE