cDir=$PWD
NodeName=node_mty


map_ta() {
   mkdir map_ta
   cd map_ta
   exec 2> err.txt
   echo "map_ta start "`date` > log.txt
   $cDir/jt_vto/runc.py --ifile list --ifield=votemper --oat --ofile=.out.nc -s --bm
   echo "map_ta end "`date` >> log.txt
   }

reduce_oa() {
   mkdir reduce_oa
   cd reduce_oa
   exec 2> err.txt
   echo "reduce_oa start "`date` > log.txt
   $cDir/jt_vto/runc.py --ifile list --ifield=votemper --oao --otc --ofile=out4.nc --bm
   echo "reduce_oa end "`date` >> log.txt
   }

mkdir $NodeName
cd $NodeName
exec 2> err.txt
echo $NodeName" start "`date` > log.txt 
map_ta | reduce_oa
echo $NodeName" end "`date` >> log.txt
