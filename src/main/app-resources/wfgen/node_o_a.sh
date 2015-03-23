cDir=$PWD
mkdir node_o_a 2> /dev/null
cd node_o_a
$cDir/jt_vto/runc.py --ifile list --ifield=votemper --oao --otc --ofile=out4.nc --bm 2> err.txt
date >> err.txt
