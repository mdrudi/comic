ResourcesDir=`dirname $0`

echo ResourcesDir= $ResourcesDir

#ls $ResourcesDir/../python/sp
#ls $ResourcesDir/../app-resources/jt_vto

cp -a $ResourcesDir/../app-resources/* .
mkdir jt_vto
cp -a $ResourcesDir/../python/sp/* ./jt_vto
touch inputfiles
cd jt_vto
ln -s sp-ciop.py run.sh

echo Remind : before submission to be generated application.xml and inputfiles
