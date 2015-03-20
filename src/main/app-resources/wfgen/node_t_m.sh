cDir=$PWD
mkdir node_t_m 2> /dev/null
cd node_t_m
$cDir/jt_vto/sp.py --ifile list --ifield=votemper --oat --ofile=.out.nc -s --bm --iClean 2> err.txt
