BinDir=`dirname $0`
FirstDate=`python $BinDir/yday-ref-01-01-1953.py $1`
FirstDate=`expr $FirstDate \* 86400`
TimeDate=`python $BinDir/yday-ref-01-01-1953.py $2`
TimeDate=`expr $TimeDate \* 86400`
LastDate=`python $BinDir/yday-ref-01-01-1953.py $3`
LastDate=`expr $LastDate \* 86400`
echo "netcdf time_counter_bnds {"
echo "dimensions:"
echo "        time = 1 ;"
echo "        nv = 2 ;"
echo "variables:"
echo "        int time(time) ;"
echo "                time:units = \"seconds since 1953-01-01 00:00:00\" ;"
echo "                time:calendar = \"standard\" ;"
echo "                time:long_name = \"time\" ;"
echo "                time:standard_name = \"time\" ;"
echo "                time:axis = \"T\" ;"
echo "                time:bounds = \"time_bnds\" ;"
echo "        int time_bnds(time, nv) ;"
echo "                time_bnds:units = \"seconds since 1953-01-01 00:00:00\" ;"
echo "data:"
echo
echo " time = $TimeDate ;"
echo
echo " time_bnds ="
echo "  $FirstDate, $LastDate ;" 
echo "}"

