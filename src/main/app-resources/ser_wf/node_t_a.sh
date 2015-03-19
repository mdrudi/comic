cDir=$PWD
mkdir node_t_a 2> /dev/null
cd node_t_a
$cDir/jt_vto/sp.py --ifile list --ifield=votemper --oat --ofile=.out.nc --bm 2> err.txt
