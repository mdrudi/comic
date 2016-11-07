#!/opt/anaconda/bin/python
# -*- coding: utf-8 -*-
# Script to discriminate a variable in a stdin file list with a magnitude threshold (it creates a new NetCDF file per
# element of the list, with a new variable named "old_variable"_threshold, with 1 in all points where
# the original variable had exceeded the threshold and 0 everywhere else).
# Paolo Oliveri, June 29, 2016
from __future__ import print_function, division
import gzip
import sys
import os
import mr
import numpy.ma as ma
import numpy as np
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

    print("threshold.py", file=sys.stderr)

    try:
        iKey = ciop.getparam('iKey')
        print("Read iKey", file=sys.stderr)
        threshold = float(ciop.getparam('Threshold'))
        print("Read Threshold", file=sys.stderr)
        Var = ciop.getparam('Var')
        print("Read Var", file=sys.stderr)
    except:
        iKey = sys.argv[1]
        threshold = float(sys.argv[2])
        Var = sys.argv[3]

    if iKey == 'None' or iKey == 'none':
        iKey = None

    try:
        AttrStr = ciop.getparam('AttrStr')
        print("Read Var Attribute String", file=sys.stderr)
    except:
        try:
            AttrStr = sys.argv[4]
        except:
            AttrStr = None
    if AttrStr == 'None' or AttrStr == 'none':
        AttrStr = None

    print("iKey: ", iKey, file=sys.stderr)
    print("threshold: " + str(threshold), file=sys.stderr)
    print("variable: ", Var, file=sys.stderr)
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
        variable_threshold = ma.where(variable_in.COSM >= threshold, 1, 0)
        variable_threshold = ma.where(variable_threshold > 1, variable_in.COSM.fill_value, variable_threshold)
        sp_bm.bm_update(sp_bm.BM_COMPUTE)
        # Attributes of Characteristic class are (StandardName,
        # VariableName, DepthLayers, LonCells, LatCells, TimeCells, ConcatenatioOfSpatialMaps, MaskedAs=None)
        variable_out = sp_type.Characteristic(StandardName='thresholded_' + variable_in.StandardName,
                                              VariableName='thresholded_' + variable_in.VariableName,
                                              DepthLayers=variable_in.DepthLayers, LonCells=variable_in.LonCells,
                                              LatCells=variable_in.LatCells, TimeCells=variable_in.TimeCells,
                                              ConcatenatioOfSpatialMaps=variable_threshold)
        OutputFileName = InputFileName[: - 3] + '_thresholded.nc'
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
