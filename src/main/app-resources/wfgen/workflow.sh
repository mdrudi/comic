. wfgen/wflib.sh

cDir=$PWD/`dirname $0`
cUP=$PWD/up
NodeName=wf

mkdir $NodeName
cd $NodeName
exec 2> err.txt
echo $NodeName" start "`date` > log.txt
ln -fs $cDir/../jt_vto jt_vto
ln -fs $cDir/../wfgen wfgen
gather $cUP | $cDir/node_vg.sh | $cDir/node_mtmg.sh | $cDir/node_mty.sh
cat node_mtmg/outcome.txt
echo $NodeName" end "`date` >> log.txt
