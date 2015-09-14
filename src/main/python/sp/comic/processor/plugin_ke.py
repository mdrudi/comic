# Plugin to compute Kinetic Energy per unit volume
from comic import type as sp_type
#import type as sp_type

lout='kinetic_energy'
lin=('u','v')

def processor(input_list):
    print 'Compute ', lout,' from ', lin
    # Select variables
    vel_x = input_list['vozocrtx']
    vel_y = input_list['vomecrty']
    #I = range(len(input_list))
    #for i in range(len(input_list)):
    #    if input_list[i].VariableName == 'vozocrtx':
    #        vel_x = input_list[i]
    #    elif input_list[i].VariableName == 'vomecrty':
    #        vel_y = input_list[i]
    rho = 1035 # (kg/m^3) Reference Density (Nemo Book 3.4)
    energy = 0.5*rho*((vel_x.COSM**2)+(vel_y.COSM**2))
    # Attributes of Characteristic class are (StandardName,VariableName,DepthLayers,LonCells,LatCells,TimeCells,ConcatenatioOfSpatialMaps=None,MaskedAs=None)
    k_energy = sp_type.Characteristic('kinetic_energy','vokenerg',vel_x.DepthLayers,vel_x.LonCells,vel_x.LatCells,vel_x.TimeCells,ConcatenatioOfSpatialMaps=energy)
    return k_energy
