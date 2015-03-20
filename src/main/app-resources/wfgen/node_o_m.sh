cDir=$PWD
mkdir node_o_m 2> /dev/null
cd node_o_m
$cDir/jt_vto/sp.py --ifile list --ifield=votemper --oao --otc --ofile=out6.nc --bm 2> err.txt
