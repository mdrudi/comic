import sys
import comic

# cd /home/melodies-wp6/ncpi/scratch/lod
# ls *nc | python jt_vto/lod.py ls 1> a
# cat a
#sea_water_salinity
#2013-07-12
#daily_mean_map
#-6.03125 30.15625 - 36.28125 45.96875
#19870101_dm-INGV--PSAL-MFSs4b3-MED-b20130712_re-fv04.00.nc
#sea_water_potential_temperature
#2013-07-12
#daily_mean_map
#-6.03125 30.15625 - 36.28125 45.96875

myin=sys.stdin.readline().replace("\r","").replace("\n","").replace(" ","").replace("\t","")
while myin :

   try : myinm=comic.ionc.ReadFile(myin,'vosaline',NoData=True)
   except: pass 
   try : myinm=comic.ionc.ReadFile(myin,'votemper',NoData=True)
   except: pass

   print myinm.StandardName
   print myinm.created
   print myinm.celltype
   print myinm.LonCells[0],myinm.LatCells[0],'-',myinm.LonCells[-1],myinm.LatCells[-1]
   print myin

   myin=sys.stdin.readline().replace("\r","").replace("\n","").replace(" ","").replace("\t","")

