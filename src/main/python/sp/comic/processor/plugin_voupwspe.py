# -*- coding: utf-8 -*-
# Plugin to compute sea water upwelling speed from sea-air wind stress input variables
# Output will be in the corner f grid
# Revision by Paolo Oliveri, Jul 22, 2016
from __future__ import print_function, division
import sys
import numpy as np
import numpy.ma as ma
from comic import type as sp_type
from seaoverland import seaoverland
from uvtofmask import uvtofmask
# from uvtotmask import uvtotmask

# np.set_printoptions(threshold=np.nan)  # It slows debugging

# Input - Output
lout = 'voupwspe'   # upwelling speed
lin = ('sozotaux', 'sometauy')

# Common Constants
rho0 = 1035  # (kg / m^3) Water reference density (NEMO Book 3.4)
EarthRadius = 6.371e6  # Earth radius (m)
deg_to_rad = np.pi / 180.0  # Sexagesimal - radiants conversion factor
EarthOmega = 2 * np.pi / 86400  # Earth angle rotation (rad/s)


# Function to calculate distance from two points in spherical coordinates
def distance(lat1, lon1, lat2, lon2):
    # sexagesimal - radiants conversion
    rdlat1 = lat1 * deg_to_rad
    rdlon1 = lon1 * deg_to_rad
    rdlat2 = lat2 * deg_to_rad
    rdlon2 = lon2 * deg_to_rad
    # Distance calculus.
    # given A(lat1, lon1) e  B(lat2, lon2) on the unit sphere we have:
    # d(A, B) = arccos( cos(lon1 - lon2) * cos(lat1) * cos(lat2) + sin(lat1) * sin(lat2) )
    distS1 = np.arccos(np.cos(rdlon1 - rdlon2) * np.cos(rdlat1) * np.cos(rdlat2) + np.sin(rdlat1) * np.sin(rdlat2))
    return distS1


# Function calculating vertical curl ( curl = dTy/dx - dTx/dy ) in interpolated t grid
# Remember to apply one point SeaOverLand expansion on input fields before calculus
def curl(tau_lat, tau_lon, lats, lons):
    taucurl = ma.array(np.empty(shape=tau_lat.shape), mask=True, fill_value=1.e20, dtype=float)
    # Vector mode
    dlat = distance(lats[2:, 1: - 1], lons[2:, 1: - 1], lats[: - 2, 1: - 1], lons[: - 2, 1: - 1])
    dlon = distance(lats[1: - 1, 2:], lons[1: - 1, 2:], lats[1: - 1, : - 2], lons[1: - 1, : - 2])
    d_lon_tau_lat = tau_lat[1: - 1, 2:] - tau_lat[1: - 1, : -2]
    d_lat_tau_lon = tau_lon[2:, 1: - 1] - tau_lon[: - 2, 1: - 1]
    taucurl[1: - 1, 1: - 1] = 1 / EarthRadius * (d_lon_tau_lat / dlon - d_lat_tau_lon / dlat)
    # Scalar mode (slow, leaved for vector code comprehension)
    # for lat in range(1, tau_lat.shape[0] - 1):
    #     for lon in range(1, tau_lat.shape[1] - 1):
    #         taucurl[lat, lon] = 1 / EarthRadius * ((tau_lat[lat, lon + 1] - tau_lat[lat, lon - 1]) /
    #                                                distance(lats[lat, lon + 1], lons[lat, lon + 1],
    #                                                         lats[lat, lon - 1], lons[lat, lon - 1]) -
    #                                                (tau_lon[lat + 1, lon] - tau_lon[lat - 1, lon]) /
    #                                                distance(lats[lat + 1, lon], lons[lat + 1, lon],
    #                                                         lats[lat - 1, lon], lons[lat - 1, lon]))
    return taucurl


# Function calculating vertical curl ( curl = dTy/dx - dTx/dy ) in native u, v grids. Output will be in corner f grid
# Remember to apply one point SeaOverLand expansion on input fields before calculus
def stagcurl(tau_lat, tau_lon, ulats, ulons, vlats, vlons):
    taucurl = ma.array(np.empty(shape=tau_lat.shape), mask=True, fill_value=1.e20, dtype=float)
    # Vector mode
    dlon = distance(ulats[:, 1:], ulons[:, 1:], ulats[:, : - 1], ulons[:, : - 1])
    dlat = distance(vlats[1:, :], vlons[1:, :], vlats[: - 1, :], vlons[: - 1, :])
    d_lon_tau_lat = tau_lat[:, 1:] - tau_lat[:, : -1]
    d_lat_tau_lon = tau_lon[1:, :] - tau_lon[: - 1, :]
    taucurl[: - 1, : - 1] = 1 / EarthRadius * (d_lon_tau_lat[: - 1, :] / dlon[: - 1, :] -
                                               d_lat_tau_lon[:, : - 1] / dlat[:, : - 1])
    # Scalar mode (slow, leaved for vector code comprehension)
    # for lat in range(1, tau_lat.shape[0] - 1):
    #     for lon in range(1, tau_lat.shape[1] - 1):
    #         taucurl[lat, lon] = 1 / EarthRadius * ((tau_lat[lat, lon + 1] - tau_lat[lat, lon]) /
    #                                                distance(ulats[lat, lon + 1], ulons[lat, lon + 1],
    #                                                         ulats[lat, lon], ulons[lat, lon]) -
    #                                                (tau_lon[lat + 1, lon] - tau_lon[lat, lon]) /
    #                                                distance(vlats[lat + 1, lon], vlons[lat + 1, lon],
    #                                                         vlats[lat, lon], vlons[lat, lon]))
    return taucurl


# Function calculating uwpwelling speed
def upspeed(tau_curl, tau_lon, f, beta0):
    up_speed_1 = (beta0 * tau_lon) / (rho0 * (f ** 2))
    up_speed_2 = tau_curl / (f * rho0)
    up_speed = up_speed_1 + up_speed_2
    return up_speed


# Main program
def processor(input_list):
    print('Compute ', lout, ' from ', lin)
    # Select variables
    sozotaux = input_list['sozotaux']
    sometauy = input_list['sometauy']
    uLatCells = sozotaux.LatCells
    uLonCells = sozotaux.LonCells
    vLatCells = sometauy.LatCells
    vLonCells = sometauy.LonCells
    staggered = False
    # Staggered grid check
    if not (np.array_equal(uLatCells, vLatCells) and np.array_equal(uLonCells, vLonCells)):
        staggered = True
        print('WARNING 21 : Input ', lin,
              ' grids are not equal. Treating them as components of a staggered C-grid.', file=sys.stderr)
    # Replicate geometry 2D (to be updated with complete model geometry variables)
    if np.ndim(sozotaux.LatCells) == 1 and np.ndim(sozotaux.LonCells) == 1:
        uLatCells = np.transpose(np.tile(sozotaux.LatCells,
                                         (sozotaux.LonCells.shape[0], 1)), (1, 0))
        uLonCells = np.tile(sozotaux.LonCells, (sozotaux.LatCells.shape[0], 1))
    if np.ndim(sometauy.LatCells) == 1 and np.ndim(sometauy.LonCells) == 1:
        vLatCells = np.transpose(np.tile(sometauy.LatCells,
                                         (sometauy.LonCells.shape[0], 1)), (1, 0))
        vLonCells = np.tile(sometauy.LonCells, (sometauy.LatCells.shape[0], 1))
    # Concatenate lat and lon cells at the centers of the grid (COMIC TYPE CHARACTERISTIC reserved procedure)
    # In C-Grid T longitudes are v longitudes and T latitudes are u latitudes
    ulats = 1 / 4 * (uLatCells[1:, 1:] + uLatCells[: - 1, 1:] +
                     uLatCells[1:, : - 1] + uLatCells[: - 1, : - 1])
    ulons = 1 / 4 * (uLonCells[1:, 1:] + uLonCells[: - 1, 1:] +
                     uLonCells[1:, : - 1] + uLonCells[: - 1, : - 1])
    vlats = 1 / 4 * (vLatCells[1:, 1:] + vLatCells[: - 1, 1:] +
                     vLatCells[1:, : - 1] + vLatCells[: - 1, : - 1])
    vlons = 1 / 4 * (vLonCells[1:, 1:] + vLonCells[: - 1, 1:] +
                     vLonCells[1:, : - 1] + vLonCells[: - 1, : - 1])
    # Cut time Dimension
    taux = sozotaux.COSM[0, ...]
    tauy = sometauy.COSM[0, ...]
    # Compute mean basin latitude
    lat0 = np.mean(vlats)
    # Compute Coriolis parameter (beta plane approximation), remember to use staggered v latitudes
    # Zero order Coriolis parameter at middle latitude
    f0 = 2 * EarthOmega * np.sin(lat0 * deg_to_rad)
    beta0 = 2 * EarthOmega * np.cos(lat0 * deg_to_rad) / EarthRadius  # First order Coriolis parameter at middle latitude
    f = f0 + beta0 * EarthRadius * (vlats - lat0) * deg_to_rad
    # Apply 1 point sea-over-land
    taux = seaoverland(taux)
    tauy = seaoverland(tauy)
    # Transport variables to T-grid before calculi (more error)
    # if staggered:
    #     print('Moving wind stress variables to t grid...', file=sys.stderr)
    #     taux[:, 1:] = 1 / 2 * (taux[:, 1:] + taux[:, : - 1])
    #     tauy[1:, :] = 1 / 2 * (tauy[1:, :] + tauy[: - 1, :])
    #     # Place t-Grid recalculated mask
    #     tmask = uvtotmask(sozotaux.COSM.mask, sometauy.COSM.mask)
    #     taux = ma.masked_where(tmask[0, ...], taux)
    #     tauy = ma.masked_where(tmask[0, ...], tauy)
    #     staggered = False
    # Compute vertical curl
    if staggered:
        vertical_curl = stagcurl(tauy, taux, ulats, ulons, vlats, vlons)
        # Load correct F mask from input fields
        fmask = uvtofmask(sozotaux.COSM.mask, sometauy.COSM.mask)
        # Shift taux to f-grid
        ftaux = ma.array(taux, mask=taux.mask, fill_value=1.e20, dtype=float)
        ftaux[:, : - 1] = (taux[:, 1:] + taux[:, : - 1]) / 2
        ftaux = ma.masked_where(fmask[0, ...], ftaux)
    else:
        vertical_curl = curl(tauy, taux, ulats, vlons)
        ftaux = taux
        fmask = sozotaux.COSM.mask
    # Compute upwelling speed and replace mask with the original one
    upwelling_speed = ma.array(np.empty(shape=sozotaux.COSM.shape), mask=False, fill_value=1.e20, dtype=float)
    # conversion from m/s to mm/s for vertical speeds
    upwelling_speed[0, ...] = upspeed(vertical_curl, ftaux, f, beta0) * 1000
    upwelling_speed = ma.masked_where(fmask, upwelling_speed)
    # Attributes of Characteristic class are (StandardName,
    # VariableName, DepthLayers, LonCells, LatCells, TimeCells, ConcatenatioOfSpatialMaps, MaskedAs=None)
    up_speed = sp_type.Characteristic(StandardName='upwelling_speed',
                                      VariableName='voupwspe', DepthLayers=None,
                                      LonCells=sozotaux.LonCells, LatCells=sometauy.LatCells,
                                      TimeCells=sozotaux.TimeCells, ConcatenatioOfSpatialMaps=upwelling_speed)
    return up_speed
