cDir=$PWD
mkdir node_g_a 2> /dev/null
cd node_g_a
date >> err.txt
$cDir/jt_vto/node_g.py 4 2> err.txt
