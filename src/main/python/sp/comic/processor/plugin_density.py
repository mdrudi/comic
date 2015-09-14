# -*- coding: utf-8 -*-
import numpy as np
from comic import type as sp_type
#import type as sp_type

lout='density'
lin=('votemper','vosaline')

# Define Constants
Pi = 3.14159
Density0 = 1035 # (kg/m^3) Reference Density (Nemo Book 3.4)

# Define Pressure function 
def whoi_z2p(z,lat): 
# ftp://ecco2.jpl.nasa.gov/data1/matlab/whoi/pressure.m
# Computes pressure given the depth at some latitude
# P=PRESSURE(D,LAT) gives the pressure P (dbars) at a depth D (m)
# at some latitude LAT (degrees).
# This probably works best in mid-latitude oceans, if anywhere!
# Ref: Saunders, "Practical Conversion of Pressure to Depth", J. Phys. Oceanog., April 1981.
# Notes: RP (WHOI) 2/Dec/91
# I copied this directly from the UNESCO algorithms
# CHECK VALUE: P=7500.004 dbar for LAT=30¬∞, DEPTH=7321.45 meters 
    PLAT = abs(lat*Pi/180)
    D = np.sin(PLAT)
    C1 = 5.92E-3+(D*D)*5.25E-3
    p = ((1-C1)-np.sqrt(((1-C1)*(1-C1))-(8.84E-6*z)))/4.42E-6
    return p

# Define Density functions
def mfs_rho0(PT,S):
# See references on Millero F.J. and Poisson A. (1981): 
# International one-atmosphere equation of state of seawater, 
# Deep-Sea Research, 28A, No. 6, pp. 625-629.
# Salinity S in ppt, Potential Temperature PT in ¬∞C
    rho00 = 999.842594 + ((((6.536336E-9*PT - \
        1.120083E-6)*PT + 1.001685E-4)*PT \
        - 9.095290E-3)*PT + 6.793952E-2)*PT
    SR = np.sqrt(abs(S))
    A = 8.244930E-1 + (((5.387500E-9*PT - 8.246700E-7)*PT + 7.643800E-5)*PT - 4.08990E-3)*PT
    B = -5.724660E-3 + (-1.654600E-6*PT + 1.022700E-4)*PT
    C = 4.831400E-4
    rho0 = rho00 + A*S + B*SR*SR*SR + C*S*S
    return rho0 
def mfs_pot_rho(S,PT,PP,rho0):
# See references on Jackett D.R. and McDougall T.J. (1995): 
# Minimal adjustment of Hydrographic Profiles to achieve Static Stability, 
# Journal of Atmospheric and Oceanic Technology, 12, pp. 381-389.
# Salinity S in ppt, Potential Temperature PT in ¬∞C, Pressure PP in bar
    SR = np.sqrt(abs(S))
    P = 0*PP/10.               # bar
    K = 1.965933E4 + \
     (((-4.190253E-5*PT + 9.648704E-3)*PT - 1.706103E0)*PT + 1.444304E2)*PT + \
     (((-5.084188E-5*PT + 6.283263E-3)*PT - 3.101089E-1)*PT + 5.284855E1)*S + \
     ((-4.619924E-4*PT + 9.085835E-3)*PT + 3.886640E-1)*SR*SR*SR + \
     ((((6.207323E-10*PT + 6.128773E-8)*PT - 2.040237E-6)*S + (1.394680E-7*PT - 1.202016E-5)*PT + 2.102898E-4)*P + 1.480266E-4*SR*SR*SR + ((2.059331E-7*PT - 1.847318E-4)*PT + 6.704388E-3)*S + ((1.956415E-6*PT - 2.984642E-4)*PT + 2.212276E-2)*PT + 3.186519E0)*P
    pot_rho = rho0/(1 - (P/K))
    return pot_rho

def processor(input_list):
    print 'Compute ', lout,' from ', lin
    # Select variables
    temp = input_list['votemper']
    salt = input_list['vosaline']
    #I = range(len(input_list))
    #for i in I:
    #    if input_list[i].VariableName == 'votemper':
    #        temp = input_list[i]
    #    elif input_list[i].VariableName == 'vosaline':
    #        salt = input_list[i]
    # Define matrix dimensions
    ntim = len(temp.COSM[:,0,0,0])
    nlev = len(temp.COSM[0,:,0,0])
    nlat = len(temp.COSM[0,0,:,0])
    nlon = len(temp.COSM[0,0,0,:])
    #N = range(nlat)
    M = range(nlon)
    L = range(nlev)
    # Compute Pressure
    pressure = np.empty(shape=(ntim,nlev,nlat,nlon))
    for m in M:
        for l in L:
            pressure[0,l,:,m] = whoi_z2p(temp.COSM[0,l,0,0],temp.COSM[0,0,:,0])
    #print "Shape of pressure: ", pressure.shape
    # Compute Potential Density field
    rho_0 = np.empty(shape=(ntim,nlev,nlat,nlon))
    rho_0 = mfs_rho0(temp.COSM,salt.COSM)
    #print "Shape of rho_0: ", rho_0.shape
    pot_density = np.empty(shape=(ntim,nlev,nlat,nlon))
    pot_density = mfs_pot_rho(salt.COSM,temp.COSM,pressure,rho_0)
    # Attributes of Characteristic class are (StandardName,VariableName,DepthLayers,LonCells,LatCells,TimeCells,ConcatenatioOfSpatialMaps=None,MaskedAs=None)
    potential_d = sp_type.Characteristic('potential_density','vopotden',temp.DepthLayers,temp.LonCells,temp.LatCells,temp.TimeCells,ConcatenatioOfSpatialMaps=pot_density)
    return potential_d

