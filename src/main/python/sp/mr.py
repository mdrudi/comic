import sys

class mr :

   def __init__(self) :
      pass

   def PushRecord(self,value,key=None) :
      if key is None : 
         print value
         #print >>sys.stderr, 'Output record :',value
      else : 
         for iKey in key : 
            print iKey+","+value+"\n"
            #print >>sys.stderr, 'Output record :',iKey+","+value+"\n"
      sys.stdout.flush

   def ClosePushRecordMap(self) : pass
   def ClosePushRecordReuce(self) : pass

   def PullRecord(self,reKeySelector=None) : 
      import sys
      import re
      a=sys.stdin.readline()
      a=a.replace("\r","").replace("\n","").replace(" ","").replace("\t","")
      if reKeySelector is None :
         return a
      else : 
         while a != '' :
            #good=False
            if re.search(reKeySelector,a.split(",")[0]) is not None : #good=True
               return a
            #if good : return a
            else : 
               a=sys.stdin.readline()
               a=a.replace("\r","").replace("\n","").replace(" ","").replace("\t","")
         return False
