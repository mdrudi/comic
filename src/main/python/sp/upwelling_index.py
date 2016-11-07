#!/opt/anaconda/bin/python
# -*- coding: utf-8 -*-
# Script to compute upwelling index field. Need as input upwelling speed field and operates a mean subtraction
# and variance division (it creates a new NetCDF file per element of the list, with a new variable named OutField and
# values V = \frac{v - \mi}{\sigma}
# Paolo Oliveri, August 31, 2016
from __future__ import print_function, division
import gzip
import sys
import os
import mr
from comic import ionc as sp_ionc
from comic import type as sp_type
from comic import bmmng as sp_bm
# np.set_printoptions(threshold=np.nan)  # It slows debugging
mymr = mr.mr()


# import the ciop functions (e.g. copy, log)
try:
    import cioppy            # as ciop #classic python, not anaconda
    ciop = cioppy.Cioppy()   # anaconda
except:
    pass


def main():
    # from calendar import monthrange,isleap
    try:
        os.chdir(os.environ['TMPDIR'])
        print("Change dir to", os.environ['TMPDIR'], file=sys.stderr)
    except:
        print("Issue to change dir, working in current dir", file=sys.stderr)

    print("upwelling_index.py", file=sys.stderr)

    try:
        iKey = ciop.getparam('iKey')
        print("Read iKey", file=sys.stderr)
        Mean = float(ciop.getparam('Mean'))
        print("Read Mean", file=sys.stderr)
        Variance = float(ciop.getparam('Variance'))
        print("Read Variance", file=sys.stderr)
        Var = ciop.getparam('Var')
        print("Read Var", file=sys.stderr)
        OutField = ciop.getparam('OutField')
        print("Read OutField", file=sys.stderr)

    except:
        iKey = sys.argv[1]
        Mean = float(sys.argv[2])
        Variance = float(sys.argv[3])
        Var = sys.argv[4]
        OutField = sys.argv[5]

    if iKey == 'None' or iKey == 'none':
        iKey = None

    try:
        AttrStr = ciop.getparam('AttrStr')
        print("Read Var Attribute String", file=sys.stderr)
    except:
        try:
            AttrStr = sys.argv[6]
        except:
            AttrStr = None
    if AttrStr == 'None' or AttrStr == 'none':
        AttrStr = None

    print("iKey: ", iKey, file=sys.stderr)
    print("Mean: " + str(Mean), file=sys.stderr)
    print("Variance: " + str(Variance), file=sys.stderr)
    print("Input variable: ", Var, file=sys.stderr)
    print("Output variable: ", OutField, file=sys.stderr)
    print("Attribute string: ", AttrStr, file=sys.stderr)
    sp_bm.bm_update(sp_bm.BM_INIT)
    InputPathFileName = mymr.PullValue(iKey)
    while InputPathFileName:
        try:
            ciop.log('INFO', 'input: ' + InputPathFileName)
            InputPathFileName = ciop.copy(InputPathFileName, os.environ['TMPDIR'])
        except:
            pass
        print("Input ", InputPathFileName, file=sys.stderr)
        InputFileName = os.path.basename(InputPathFileName)
        if InputPathFileName[-3:] == '.gz':
            inF = gzip.open(InputPathFileName, 'rb')
            InputPathFileName = InputPathFileName[-3:]
            InputFileName = InputFileName[-3:]
            outF = open(InputPathFileName, 'wb')
            outF.write(inF.read())
            inF.close()
            outF.close()
        variable_in = sp_ionc.ReadFile(InputPathFileName, Var)
        sp_bm.bm_update(sp_bm.BM_READ, variable_in.COSM)
        variable_calc = (variable_in.COSM - Mean) / Variance
        sp_bm.bm_update(sp_bm.BM_COMPUTE)
        # Attributes of Characteristic class are (StandardName,
        # VariableName, DepthLayers, LonCells, LatCells, TimeCells, ConcatenatioOfSpatialMaps, MaskedAs=None)
        variable_out = sp_type.Characteristic(StandardName=OutField, VariableName=OutField,
                                              DepthLayers=variable_in.DepthLayers, LonCells=variable_in.LonCells,
                                              LatCells=variable_in.LatCells, TimeCells=variable_in.TimeCells,
                                              ConcatenatioOfSpatialMaps=variable_calc)
        OutputFileName = InputFileName[: - 3] + '_uidx.nc'
        if AttrStr is not None:
            import json
            Attributes = json.loads(AttrStr)
            if variable_out.VariableName in Attributes:
                variable_out.SetAttributes(Attributes[variable_out.VariableName])
            if 'global' in Attributes:
                sp_ionc.WriteFile(variable_out, OutputFileName, Attributes['global'])
            else:
                sp_ionc.WriteFile(variable_out, OutputFileName)
        else:
            sp_ionc.WriteFile(variable_out, OutputFileName)
        sp_bm.bm_update(sp_bm.BM_WRITE, variable_out.COSM)
        InputPathFileName = mymr.PullValue(iKey)
        try:
            print("Publishing output by ciop " + os.getcwd() + '/' + OutputFileName, file=sys.stderr)
            ciop.publish(os.environ['TMPDIR'] + '/' + OutputFileName, metalink=False)
            ciop.publish(os.environ['TMPDIR'] + '/' + OutputFileName, metalink=True)
        except:
            print("Issue to publish by ciop " + os.getcwd() + '/' + OutputFileName, file=sys.stderr)
        print("Publishing output by mr module", file=sys.stderr)
        mymr.PushRecord(os.getcwd() + '/' + OutputFileName)
        sys.stdout.flush()


if __name__ == "__main__":
    # import sp_bm
    sp_bm.bm_setup()
    main()
    sp_bm.bm_update(sp_bm.BM_WRAP)
    sp_bm.bm_close()
    try:
        pathname = os.environ['TMPDIR'] + '/bm.txt_' + os.environ['mapred_task_id']
        os.rename('bm.txt', pathname)
        ciop.publish(pathname)
    except:
        print("Issue to publish by ciop benchmarking info", file=sys.stderr)
