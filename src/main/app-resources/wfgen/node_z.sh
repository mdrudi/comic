#!/bin/sh

mkdir node_z 2> /dev/null
cd node_z

exec 2> err.txt 

while read filename; do
   #echo $filename
   num_c=`basename $filename | wc -c`
   num_c_3=`expr $num_c - 3`
   #echo $num_c $num_c_3
   este=`basename $filename| cut -c $num_c_3-`
   if [ "$este" = ".gz" ]; then
      num_c_3c=`expr $num_c_3 - 1`
      outfile=$PWD/`basename $filename| cut -c -$num_c_3c`
      gzip -c -d $filename > $outfile
      echo $outfile
   else :
      ln -fs $filename
      echo $PWD/`basename $filename`
      fi

   numfile=`ls -1 | wc -l`
   while [ $numfile -gt 31 ]; do
      echo $numfile >> err.txt
      sleep 10
      numfile=`ls -1 | wc -l`
      done

   done
