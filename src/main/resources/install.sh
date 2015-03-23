ResourcesDir=`dirname $0`

echo ResourcesDir= $ResourcesDir

cp -a $ResourcesDir/../app-resources/* .
mkdir jt_vto
cp -a $ResourcesDir/../python/sp/* ./jt_vto
#touch inputfiles
cd jt_vto
ln -sf spciop.py run.py
ln -sf sp.py runc.py

echo Remind : before submission map-reduce workflow, to be generated the following files : application.xml , inputfiles
echo NB : to run from command line, useful commands are in dir jt_vto ;
echo "     tools to handle a workflow in parallel or standard environment are in dir wfgen"
