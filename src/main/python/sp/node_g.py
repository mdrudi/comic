#!/usr/bin/python

import os

# import the ciop functtons (e.g. copy, log)
import sys
sys.path.append('/usr/lib/ciop/python/')
import cioppy as ciop

def GetLine(keyPattern=None) :
   import sys
   import re
   a=sys.stdin.readline().replace("\r","").replace("\n","").replace(" ","").replace("\t","")
   while a != '' :
      #print "checking ",a[-3:]+'f'
      good=False

      if keyPattern is None : good=True
      elif re.search(keyPattern,a) is not None : good=True

      if good : return a
      print "Dump ",a
      a=sys.stdin.readline().replace("\r","").replace("\n","").replace(" ","").replace("\t","")

   return False



lib=dict()



def main():
   try : 
      os.chdir(os.environ['TMPDIR'])
      print "Change dir to", os.environ['TMPDIR'] 
   except : print "Issue to change dir, working in current dir"

   print "node_g.py"

   #opt['InFile']=ciop.getparam('InFile')   #MANDATORY
   try : 
      iKey=ciop.getparam('iKey')
      print "Read selection key "
   except : iKey=None
   print "Selection key: ",iKey

   InputPathFileName=GetLine(iKey)
   while InputPathFileName :
      InputFileName=os.path.basename(InputPathFileName)      
      month=InputFileName[0:6]
      if month in lib.keys() :
         list_files=lib[month]
         list_files.append(InputPathFileName)
      else :
         list_files=list()
         list_files.append(InputPathFileName)
         lib[month]=list_files
      print month,InputFileName,InputPathFileName
      InputPathFileName=GetLine(iKey)

   for month in lib.keys() :
      out_file_name="last"+month+".txt"
      out_file = open(out_file_name,"w")
      print out_file_name
      for InputPathFileName in lib[month] :
         out_file.write(InputPathFileName+"\n")
      out_file.close()
      try : 
         print "Publishing by ciop", out_file_name
         ciop.publish(os.environ['TMPDIR']+'/'+out_file_name)
      except : print "Issue to plublish by ciop"

if __name__ == "__main__":
   main()

