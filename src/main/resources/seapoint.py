import sp_ionc as io


myVotemper=io.ReadFile("/tmp/20150410_dm-INGV--TEMP-MFSs4d-MED-b20150331_fc-fv04.00.nc","votemper")

print myVotemper.COSM.mask.shape,myVotemper.COSM.size
for ilevel in range(myVotemper.COSM.shape[1]) :
   print "y("+str(ilevel+1)+")="+str(myVotemper.COSM[0,ilevel,:,:].count())
print myVotemper.COSM.count()
