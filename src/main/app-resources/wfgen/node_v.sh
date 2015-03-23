cDir=$PWD
mkdir node_v 2> /dev/null
cd node_v
$cDir/jt_vto/runc.py --ifile list --ifield=votemper --oav='[0,10,50,100,500,1000,2000]' --bm --iClean 2> err.txt
