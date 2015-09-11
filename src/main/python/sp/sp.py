#!/opt/anaconda/bin/python

import sys
import os

#import sp_glob
#import sp_type
#from sp_ionc import ReadFile, WriteFile
#import sp_bm
import mr
mymr=mr.mr()
import comic
from comic import bmmng as sp_bm

#sp_glob.verbose=False

#center of input layer : 1.47 4.58 7.94 11.55
# input layers         : 0 - 2.94 - 6.22 - 9.66 - 13.44
# input thickness      : 2.94 3.28 3.44 3.78

##### PUBLIC FUNCTIONALITIES : START

def ParseRange ( opt ) :
   import numpy
   import json
   #return numpy.array(map(float,opt.replace(" ","").replace("[","").replace("]","").split(",")))
   return numpy.array(json.loads(opt))

def GetLine(opt_bm,keyPattern=None,stream=sys.stdin) :
   import sys
   import re
   if stream is sys.stdin :
      if opt_bm : sp_bm.bm_update(sp_bm.BM_INIT)
      a=mymr.PullValue(keyPattern)
      if opt_bm : sp_bm.bm_update(sp_bm.BM_IDLE)
      return a
   else :
      if opt_bm : sp_bm.bm_update(sp_bm.BM_INIT)
      a=stream.readline()
      if opt_bm : sp_bm.bm_update(sp_bm.BM_IDLE)
      a=a.replace("\r","").replace("\n","").replace(" ","").replace("\t","")
      if a != '' : return a
      else : return False
# whether read from file, non need of keyPattern
#      while a != '' :
#         good=False
#         if keyPattern is None : good=True
#         elif re.search(keyPattern,a) is not None : good=True
#         if good : return a
#         if opt_bm : sp_bm.bm_update(sp_bm.BM_INIT)
#         a=stream.readline()         #.replace("\r","").replace("\n","").replace(" ","").replace("\t","")
#         if opt_bm : sp_bm.bm_update(sp_bm.BM_IDLE)
#         a=a.replace("\r","").replace("\n","").replace(" ","").replace("\t","")
#      return False

def EchoInputFile(text) :
   print >>sys.stderr, 'Input File  :',text

def EchoOutputFile(text,key=None) :
   #print text
   #sys.stdout.flush
   if key is None : mymr.PushRecord(text)
   else : mymr.PushRecord(text,(key,))
   print >>sys.stderr, 'Output File :',text

def NoneOrList(ar) :
   if ar is None : return None
   return ar.tolist()

##### PUBLIC FUNCTIONALITIES : END



##### LOCAL FUNCTIONALITIES : START

#http://stackoverflow.com/questions/301134/dynamic-module-import-in-python

#http://stackoverflow.com/questions/8525765/load-parameters-from-a-file-in-python
class Params(object):
   def __init__(self, input_file_name):
      with open(input_file_name, 'r') as input_file:
         for line in input_file:
            #print line
            row = line.split("#")[0].split("=")
            label = row[0].replace(" ","").replace("\r","").replace("\n","")
            if label != "" :
               data = row[1].replace(" ","").replace("\r","").replace("\n","")  # rest of row is data list
               self.__dict__[label] = data #values if len(values) > 1 else values[0]


class tag_op :

   def __init__(self) :
      import optparse

      parser = optparse.OptionParser()
      parser.add_option("--ifile",     dest="MyInputFile",     default="none",   metavar="InFile",       help="read data from file InFile (netcdf format) ; if InFile='list' then read data from the list of files which names are passed in standard input") 
      parser.add_option("--ifield",    dest="MyInputVariable", metavar="Var",    help="working variable to be read from input file/s")
      parser.add_option("--ilonlat",   dest="LonLat",          default=None,     metavar="LonLat",       help="optional - spatial working domain - default : the whole in input")
      parser.add_option("--ikey",      dest="iKey",            default=None,     metavar="iKey",         help="optional - input selection mapreduce key/s")
      parser.add_option("--iClean",    dest="iClean",          default=False,    action="store_true",    help="flag to remove the input file after reading")
      parser.add_option("--iattrf",    dest="AttrFile",        default=None,     metavar="AttrFile",     help="optional - file with template for metadata in output netcdf file")
      parser.add_option("--iattrs",    dest="AttrStr",         default=None,     metavar="AttrStr",      help="optional - string with template for metadata in output netcdf file")
      parser.add_option("--ofile",     dest="MyOutFile",       default="out.nc", metavar="OutFile",      help="optional - file name for output or postfix in case of multiple output files - default 'out.nc'")
      parser.add_option("--oat",       dest="oat",             default=None,     action="store_true",    help="flag to activate the computation of average value over time")
      parser.add_option("--oac",       dest="oac",             default=None,     action="store_true",    help="flag to activate the computation of climatological average value over time")
      parser.add_option("--oav",       dest="oav",             default=None,     metavar="OutLayer" ,    help="flag to activate the computation of average value over spatial depth layers given here as parameter") 
      parser.add_option("--oao",       dest="oao",             default=None,     action="store_true",    help="flag to activate the computation of average value over the spatial lon lat plane")
      parser.add_option("--otc",       dest="otc",             default=None,     action="store_true",    help="flag to concatenate output along the time dimension into one single output file")
      parser.add_option("--okey",      dest="oKey",            default=None,     metavar="oKey",         help="optional - output mapreduce key")
      parser.add_option("-v",          dest="verbose",         default=False,    action="store_true",    help="legacy - be verbose")
      parser.add_option("-p",          dest="MyParameterFile", default='none',   metavar="ParFile",      help="legacy - alternative parameter file to provide var , lout, lon, lat")
      parser.add_option("--bm",        dest="bm",              default=False,    action="store_true",    help="print and save benchmarking information")
      parser.add_option("-s",          dest="SpeedUp",         default=False,    action="store_true",    help="might use more memory and improve the execution speed")
      (options, args) = parser.parse_args()
      #print options
      #print args

      if options.MyParameterFile != 'none' :
         #print options.MyParameterFile
         #exec "import %s" % options.MyParameterFile
         params = Params(options.MyParameterFile)
         #print options.MyInputFile
         if options.MyInputFile == 'none' : 
            #print options.MyInputFile
            options.MyInputFile=params.MyInputFile
         options.MyInputVariable=params.MyInputVariable
         options.MyOutputLayer=params.MyOutputLayer
         if ~ hasattr(params,"MyOutputLon") : params.MyOutputLon=None
         options.MyOutputLon=params.MyOutputLon
         if ~ hasattr(params,"MyOutputLat") : params.MyOutputLat=None
         options.MyOutputLat=params.MyOutputLat

      if options.oav is not None :
         self.OutLayer=ParseRange(options.oav) 
      else :
         self.OutLayer=None

      if options.LonLat is not None :
         #import numpy
         #import json
         #self.LonLat=numpy.array(json.loads(options.LonLat))
         self.LonLat=ParseRange(options.LonLat)
      else :
         self.LonLat=None

      if options.oao is not None :
         self.oao=True
      else :
         self.oao=None

      if options.otc is not None :
         self.otc=True
      else :
         self.otc=None

      self.InFile=options.MyInputFile
      self.iKey=options.iKey
      self.Variables=options.MyInputVariable
      self.iClean=options.iClean
      self.OutFile=options.MyOutFile
      self.bm=options.bm
      self.s=options.SpeedUp
      self.v=options.verbose
      self.oat=options.oat
      self.oac=options.oac
      self.oKey=options.oKey
      self.AttrFile=options.AttrFile
      self.AttrStr=options.AttrStr


def Many2OneBlock (opt_bm,my_sp,InitFileName,keyPattern,type=None,outputKey=None) :
   import sys
   if type == "stream" :
      stream=open(InitFileName)
      InputFileName=GetLine(opt_bm,keyPattern,stream)
   else :
      InputFileName=InitFileName
      stream=sys.stdin
   one=False
   while InputFileName :
      one=True
      EchoInputFile(InputFileName)
      my_sp.loop_go(InputFileName)
      InputFileName=GetLine(opt_bm,keyPattern,stream)
   if one :
      output_name=my_sp.loop_close()
      EchoOutputFile(output_name,outputKey)


##### LOCAL FUNCTIONALITIES : END






##### COMMAND LINE FRONT END : START


def main():
   import re
   #import time   #test to use time.sleep
   sp_bm.bm_setup()

   print >>sys.stderr, "sp.py"
   print >>sys.stderr, "available processors :",comic.processor.dict

   opt=tag_op()

   if opt.v :
      comic.glob.verbose=True
   
   VSpaceAverage=(opt.OutLayer is not None) 
   TimeAverage=(opt.oat is not None or opt.oac is not None)
   OSpaceAverage=(opt.oao is not None) 
   One2One=(opt.InFile != 'list')
   Many2One=(opt.InFile == 'list') and ( TimeAverage or opt.otc is not None )
   Many2Many=(opt.InFile == 'list') and not TimeAverage and opt.otc is None

   print >>sys.stderr, "\nInput"
   print >>sys.stderr, " Input File/s    : ", opt.InFile
   print >>sys.stderr, " Selection Key   : ", opt.iKey
   print >>sys.stderr, " Attribute File  : ", opt.AttrFile
   print >>sys.stderr, " Attribute String: ", opt.AttrStr
   print >>sys.stderr, "\nWorking Domain"
   print >>sys.stderr, " Variable/s      : ", opt.Variables
   print >>sys.stderr, " Time Range      :  None"
   print >>sys.stderr, " Depth Range     :  None"
   print >>sys.stderr, " Lon x Lat Range : ", NoneOrList(opt.LonLat)    #.tolist()
   print >>sys.stderr, "\nComputation"
   print >>sys.stderr, " Grid - Time      : ", opt.oat
   print >>sys.stderr, " Grid - Climatological Time      : ", opt.oac
   print >>sys.stderr, " Grid - Layer     : ", NoneOrList(opt.OutLayer)  #.tolist()
   print >>sys.stderr, " Grid - Lon x Lat : ", opt.oao
   print >>sys.stderr, "\nOutput"
   if Many2Many : 
      print >>sys.stderr, " File             : [InputFile]+", opt.OutFile
   else :
      print >>sys.stderr, " File             : ", opt.OutFile
   print >>sys.stderr, " Output Key       : ", opt.oKey
   print >>sys.stderr, "\nBehaviour--------"
   print >>sys.stderr, "\nWhich Operation"
   print >>sys.stderr, " average over vertical space  :",VSpaceAverage
   print >>sys.stderr, " average over orizontal space :",OSpaceAverage
   print >>sys.stderr, " average over time            :",TimeAverage
   print >>sys.stderr, "\nWhich I/O Flow Schema"
   print >>sys.stderr, " many to many :",Many2Many
   print >>sys.stderr, " many to one  :",Many2One
   print >>sys.stderr, " one to one   :",One2One
   print >>sys.stderr, "\n"
   print >>sys.stderr, "\nExecution-------"

   if opt.iKey is not None :
      keyPattern=re.compile(opt.iKey)
   else :
      keyPattern=None

   if opt.bm : sp_bm.bm_update(sp_bm.BM_INIT)

   #my_sp=sp(opt.Variables,opt.OutFile,opt.LonLat,opt.OutLayer,opt.bm,opt.s, OutLonLat=opt.oao , TimeAverage=TimeAverage , RemoveInput=opt.iClean )

   # many files to one file
   if Many2One : 
      #one=False
      InputFileName=GetLine(opt.bm,keyPattern)
      if InputFileName :
         if InputFileName[-4:]==".txt" :
            while InputFileName :
               #one=True
               print >>sys.stderr, "Processing group..."+InputFileName 
               EchoInputFile(InputFileName)
               my_sp=comic.pilot(opt.Variables,os.path.basename(InputFileName)+opt.OutFile,opt.LonLat,opt.OutLayer,opt.bm,opt.s, OutLonLat=opt.oao , TimeAverage=TimeAverage , ClimatologicalAverage=opt.oac , RemoveInput=opt.iClean , AttrFile=opt.AttrFile , AttrStr=opt.AttrStr )
               Many2OneBlock(opt.bm,my_sp,InputFileName,None,type="stream",outputKey=opt.oKey)
               InputFileName=GetLine(opt.bm,keyPattern)
            #if one :
            #OutputFileName=my_sp.loop_close()
            #EchoOutputFile(OutputFileName)
         else : #in this case must be InputFileName[-3:]==".nc"
            print >>sys.stderr, "Processing simple..."
            my_sp=comic.pilot(opt.Variables,opt.OutFile,opt.LonLat,opt.OutLayer,opt.bm,opt.s, OutLonLat=opt.oao , TimeAverage=TimeAverage , ClimatologicalAverage=opt.oac  , RemoveInput=opt.iClean , AttrFile=opt.AttrFile , AttrStr=opt.AttrStr )
            Many2OneBlock(opt.bm,my_sp,InputFileName,keyPattern,outputKey=opt.oKey)
   # many files to many files
   elif Many2Many : 
      my_sp=comic.pilot(opt.Variables,opt.OutFile,opt.LonLat,opt.OutLayer,opt.bm,opt.s, OutLonLat=opt.oao , TimeAverage=TimeAverage , RemoveInput=opt.iClean , AttrFile=opt.AttrFile , AttrStr=opt.AttrStr )
      InputFileName=GetLine(opt.bm,keyPattern)
      while InputFileName :
         EchoInputFile(InputFileName)
         OutputFileName=my_sp.once(InputFileName,OutFileNameIsPostfix=True)
         EchoOutputFile(OutputFileName,opt.oKey)
         #time.sleep(1)
         InputFileName=GetLine(opt.bm,keyPattern)

   # one file to one file
   elif One2One : 
      my_sp=comic.pilot(opt.Variables,opt.OutFile,opt.LonLat,opt.OutLayer,opt.bm,opt.s, OutLonLat=opt.oao , TimeAverage=TimeAverage , RemoveInput=opt.iClean , AttrFile=opt.AttrFile , AttrStr=opt.AttrStr )
      InputFileName=opt.InFile
      EchoInputFile(InputFileName)
      OutputFileName=my_sp.once(InputFileName)
      EchoOutputFile(OutputFileName)

   #nothing
   else :
      print >>sys.stderr, "Nothing to do"

   #if sp_glob.verbose : print 'Out[0,0,88,0]=',my_sp.COSM[0,0,88,0], type(my_sp.COSM[0,0,88,0]), repr(my_sp.COSM[0,0,88,0]),my_sp.COSM[:,:,88,0]

   if opt.bm : sp_bm.bm_close()



if __name__ == "__main__":
   main()

