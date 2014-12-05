ResourcesDir=`dirname $0`

echo ResourcesDir= $ResourcesDir

cp -a $ResourcesDir/../app-resources/* .
mkdir jt_vto
cp -a $ResourcesDir/../python/sp/* ./jt_vto
touch inputfiles
cd jt_vto
ln -sf sp-ciop.py run.py

echo Remind : before submission to be generated application.xml and inputfiles
echo NB : to run from command line, change your working dir to jt_vto