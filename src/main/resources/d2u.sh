Source="ftp://gnoodap.bo.ingv.it/Core/MEDSEA_REANALYSIS_PHYS_006_004/myov05-med-ingv-sal-rean-dm"
Dest="s3://melodies-wp6"

lls() {
   ncftpls -f up $1 #> filenamelist
   }

ldl() {
    mkdir $2
    while read filename; do
      echo $1/$filename >> $0.list_ldl
      ncftpget -f up $1/$filename #&> /dev/null
      mv -f $filename $2/
      echo $2/$filename
      done
   }

lul() {
   while read filename; do
      echo $filename >> $0.list_lul
      s3cmd put $filename $1
      rm $filename
      done
   }

#lls $Source/20080101_dm-INGV--TEMP-MFSs4b3-MED-b20140620_re-fv05.00.nc.gz | ldl $Source | lul $Dest/2008/
#lls $Source/yr1987/* | ldl $Source/yr1987 yr1987 | lul $Dest/1987s/
#lls $Source/yr1988/* | ldl $Source/yr1988 yr1988 | lul $Dest/1988s/
#lls $Source/2009* | ldl $Source | lul $Dest/2009/
#lls $Source/2010* | ldl $Source | lul $Dest/2010/
#lls $Source/2011* | ldl $Source | lul $Dest/2011/
#lls $Source/2012* | ldl $Source | lul $Dest/2012/

#lls $Source/yr2012/* | ldl $Source/yr2012 yr2012 | lul $Dest/2012s/
#lls $Source/yr2011/* | ldl $Source/yr2011 yr2011 | lul $Dest/2011s/
#lls $Source/yr2010/* | ldl $Source/yr2010 yr2010 | lul $Dest/2010s/

#for tYYYY in 2013 ; do
#   #tYYYY=2010
#   sTot=$Source/yr$tYYYY
#   tDir=$tYYYY
#   dDir=$Dest/${tYYYY}s/
#   lls $sTot/* | ldl $sTot $tDir | lul $dDir
#   done

Source="ftp://gnoodap.bo.ingv.it/Core/MEDSEA_REANALYSIS_PHYS_006_004/myov05-med-ingv-cur-rean-dm"

for tYYYY in 2013 ; do
   #tYYYY=2010
   sTot=$Source/yr$tYYYY
   tDir=$tYYYY
   dDir=$Dest/${tYYYY}c/
   lls $sTot/* | ldl $sTot $tDir | lul $dDir
   done

