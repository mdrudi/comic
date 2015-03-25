. wfgen/wflib.sh

cDir=$PWD
NodeName=node_mtmg

map_tm() {
   mkdir map_tm
   cd map_tm
   exec 2> err.txt
   echo "map_tm start "`date` > log.txt
   $cDir/jt_vto/runc.py --ifile list --ifield=votemper --oat --ofile=.out.nc -s --bm --iClean
   echo "map_tm end "`date` >> log.txt
   }

reduce_om() {
   mkdir reduce_om
   cd reduce_om
   exec 2> err.txt
   echo "reduce_om start "`date` > log.txt
   $cDir/jt_vto/runc.py --ifile list --ifield=votemper --oao --otc --ofile=out6.nc --bm
   echo "reduce_om end "`date` >> log.txt
   }

reduce_ga() {
   mkdir reduce_ga
   cd reduce_ga
   exec 2> err.txt
   echo "reduce_ga start "`date` > log.txt
   $cDir/jt_vto/node_g.py 4
   echo "reduce_ga end "`date` >> log.txt
   }

mkdir $NodeName
cd $NodeName
exec 2> err.txt
echo $NodeName" start "`date` > log.txt 
map_tm | passer buffer.txt | reduce_om > outcome.txt
cat buffer.txt | passer outcome.txt | reduce_ga
echo $NodeName" end "`date` >> log.txt


