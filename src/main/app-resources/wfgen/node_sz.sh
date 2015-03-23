#!/bin/sh

mkdir node_sz 2> /dev/null
cd node_sz

exec 2> err.txt 

date >> err.txt

while read filename; do
   #echo $filename
   prot=`echo $filename| cut -c 1-3`
   if [ "$prot" = "s3:" ]; then
      s3cmd get $filename >> err.txt
   else :
      prot="loc"
      fi
   num_c=`basename $filename | wc -c`
   num_c_3=`expr $num_c - 3`
   #echo $num_c $num_c_3
   este=`basename $filename| cut -c $num_c_3-`
   if [ "$este" = ".gz" ]; then
      num_c_3c=`expr $num_c_3 - 1`
      outfile=$PWD/`basename $filename| cut -c -$num_c_3c`
      if [ "$prot" = "loc" ]; then
         gzip -c -d $filename > $outfile
      else :
         gzip -d `basename $filename` 
         fi
      echo $outfile
   else :
      if [ "$prot" = "loc" ]; then
         ln -sf $filename `basename $filename`
         fi
      echo $PWD/`basename $filename`
      fi

   numfile=`ls -1 | wc -l`
   while [ $numfile -gt 31 ]; do
      echo $numfile >> err.txt
      sleep 10
      numfile=`ls -1 | wc -l`
      done

   done

date >> err.txt
