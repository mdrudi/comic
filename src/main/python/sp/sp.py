#!/usr/bin/python

#import sp_glob
#from sp_ionc import ReadFile, WriteFile

import sp_bm
sp_bm.bm_setup()

#sp_glob.verbose=False

#center of input layer : 1.47 4.58 7.94 11.55
# input layers         : 0 - 2.94 - 6.22 - 9.66 - 13.44
# input thickness      : 2.94 3.28 3.44 3.78



##### PUBLIC FUNCTIONALITIES : START

def ParseRange ( opt , Time=False ) :
   import numpy
   import json
   #return numpy.array(map(float,opt.replace(" ","").replace("[","").replace("]","").split(",")))
   if Time :
      import datetime
      tmpList=json.loads(opt)
      for i in range(len(tmpList)) :
         tmpList[i]=datetime.datetime.strptime(tmpList[i],"%Y-%m-%d %H:%M")
   else :
      tmpList=json.loads(opt)
   return numpy.array(tmpList)

def GetLine(keyPattern=None) :
   import sys
   import re
   c=10
   #a=sys.stdin.readline()
   #if a == '' : return False
   #return a.replace("\r","").replace("\n","")
   a=sys.stdin.readline().replace("\r","").replace("\n","")
   while a != '' :
      good=False
      if keyPattern is None : good=True
      elif re.search(keyPattern,a) is not None : good=True
      if good : return a
      a=sys.stdin.readline().replace("\r","").replace("\n","")
   return False

def EchoInputFile(text) :
   print 'Input File  :',text

def EchoOutputFile(text) :
   print 'Output File :',text

def NoneOrList(ar) :
   import datetime
   if ar is None : return None
   if len(ar) and type(ar[0]) is datetime.datetime : 
      return ar
   else : 
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
      import datetime 

      parser = optparse.OptionParser()
      parser.add_option("--ifile",   dest="MyInputFile",     default="none",   metavar="InFile",    help="read data from file InFile (netcdf format) ; if InFile='list' then read data from the list of files which names are passed in standard input") 
      parser.add_option("--ifield",  dest="MyInputVariable", default=None,     metavar="Var",    help="working variable to be read from input file/s")
      parser.add_option("--ilonlat", dest="LonLat",          default=None,     metavar="LonLat",    help="optional - spatial working domain - default : the whole in input")
      parser.add_option("--ikey",    dest="iKey",            default=None,     metavar="iKey",      help="optional - input selection key")
      parser.add_option("--iClean",  dest="iClean",          default=False,    action="store_true", help="flag to remove the input file after reading")
      parser.add_option("--ofile",   dest="MyOutFile",       default="out.nc", metavar="OutFile",   help="optional - file name for output or postfix in case of multiple output files - default 'out.nc'")
      parser.add_option("--oat",     dest="oat",             default=None,     metavar="OutTRange", help="flag to activate the computation of average value over time range given here as parameter")     #action="store_true",
      parser.add_option("--oav",     dest="oav",             default=None,     metavar="OutLayer" , help="flag to activate the computation of average value over spatial depth layers given here as parameter") 
      parser.add_option("--oao",     dest="oao",             default=None,     action="store_true", help="flag to activate the computation of average value over the spatial lon lat plane")
      parser.add_option("--otc",     dest="otc",             default=None,     action="store_true", help="flag to concatenate output along the time dimension into one single output file")
      parser.add_option("--ofc",     dest="ofc",             default=None,     metavar="OutField",  help="flag to activate the computation of new field")
      parser.add_option("-v",        dest="verbose",         default=False,    action="store_true", help="legacy - be verbose")
      parser.add_option("-p",        dest="MyParameterFile", default='none',   metavar="ParFile",   help="legacy - alternative parameter file to provide var , lout, lon, lat")
      parser.add_option("--bm",      dest="bm",              default=False,    action="store_true", help="print and save benchmarking information")
      parser.add_option("-s",        dest="SpeedUp",         default=False,    action="store_true", help="might use more memory and improve the execution speed")
      (options, args) = parser.parse_args()

      if options.MyParameterFile != 'none' :
         params = Params(options.MyParameterFile)
         if options.MyInputFile == 'none' : 
            options.MyInputFile=params.MyInputFile
         options.MyInputVariable=params.MyInputVariable
         options.MyOutputLayer=params.MyOutputLayer
         if ~ hasattr(params,"MyOutputLon") : params.MyOutputLon=None
         options.MyOutputLon=params.MyOutputLon
         if ~ hasattr(params,"MyOutputLat") : params.MyOutputLat=None
         options.MyOutputLat=params.MyOutputLat

      if options.oat is not None :
         self.OutTRange=ParseRange(options.oat,Time=True)
      else :
         self.OutTRange=None

      if options.oav is not None :
         self.OutLayer=ParseRange(options.oav) 
      else :
         self.OutLayer=None

      if options.LonLat is not None :
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

      if options.ofc is not None :
         self.OutField=options.ofc
      else :
         self.OutField=None

      self.InFile=options.MyInputFile
      self.iKey=options.iKey
      self.Variables=options.MyInputVariable
      self.iClean=options.iClean
      self.OutFile=options.MyOutFile
      self.bm=options.bm
      self.s=options.SpeedUp
      self.v=options.verbose

##### LOCAL FUNCTIONALITIES : END






##### COMMAND LINE FRONT END : START

def main():
   import re
   #sp_bm.bm_setup()
   import comic

   print "sp.py"
   print "available processors :",comic.processor.dict

   opt=tag_op()

   if opt.v :
      #sp_glob.verbose=True
      comic.glob.verbose=True

   if opt.OutField is not None :     #in comic.processor.dict) :
#      print "WARNING : forcing the output variable"
#      opt.OutField=opt.Variables
#   else :
      print "WARNING : forcing the input variable"
      opt.Variables=comic.processor.dict[opt.OutField][0]
      print "WARNING : forcing the operation flags to ensure the correct behaviour"
      opt.OutTRange=None
      opt.OutLayer=None
      opt.oao=None

   VSpaceAverage=(opt.OutLayer is not None) 
   TimeAverage=(opt.OutTRange is not None)
   OSpaceAverage=(opt.oao is not None) 
   FieldComputation=(opt.OutField is not None)
   One2One=(opt.InFile != 'list')
   Many2One=(opt.InFile == 'list') and ( TimeAverage or opt.otc is not None or FieldComputation )
   Many2Many=(opt.InFile == 'list') and not TimeAverage and opt.otc is None and not FieldComputation

   print "\nInput"
   print " Input File/s     : ", opt.InFile
   print " Selection Key    : ", opt.iKey
   print "\nWorking Domain"
   print " Variable/s       : ", opt.Variables
   print " Time Range       :  None"
   print " Depth Range      :  None"
   print " Lon x Lat Range  : ", NoneOrList(opt.LonLat)
   print "\nComputation"
   print " Grid - Time      : ", NoneOrList(opt.OutTRange)
   print " Grid - Layer     : ", NoneOrList(opt.OutLayer)
   print " Grid - Lon x Lat : ", opt.oao
   print " Field            : ", opt.OutField
   print "\nOutput"
   if Many2Many : 
      print " File             : [InputFile]+", opt.OutFile
   else :
      print " File             : ", opt.OutFile
   print "\nBehaviour--------"
   print "\nWhich Operation"
   print " average over vertical space  :",VSpaceAverage
   print " average over orizontal space :",OSpaceAverage
   print " average over time            :",TimeAverage
   print " compute new field            :",FieldComputation
   print "\nWhich I/O Flow Schema"
   print " many to many :",Many2Many
   print " many to one  :",Many2One
   print " one  to one  :",One2One
   print "\n"
   print "\nExecution-------"

   if opt.iKey is not None :
      keyPattern=re.compile(opt.iKey)
   else :
      keyPattern=None

   if opt.bm : sp_bm.bm_update(sp_bm.BM_INIT)

   if FieldComputation :
      my_sp=comic.pilot(opt.OutField,opt.OutFile,opt.LonLat,opt.OutLayer,opt.bm,opt.s, OutLonLat=opt.oao , TimeRange=opt.OutTRange , RemoveInput=opt.iClean )
   else :   
      my_sp=comic.pilot(opt.Variables,opt.OutFile,opt.LonLat,opt.OutLayer,opt.bm,opt.s, OutLonLat=opt.oao , TimeRange=opt.OutTRange , RemoveInput=opt.iClean )

   # many files to one file
   if Many2One : 
      one=False
      InputFileName=GetLine(keyPattern)
      while InputFileName :
         one=True 
         EchoInputFile(InputFileName)
         my_sp.loop_go(InputFileName)
         InputFileName=GetLine(keyPattern)
      if one :
         OutputFileName=my_sp.loop_close()
         EchoOutputFile(OutputFileName)

   # many files to many files
   elif Many2Many : 
      InputFileName=GetLine(keyPattern)
      while InputFileName :
         EchoInputFile(InputFileName)
         OutputFileName=my_sp.once(InputFileName,OutFileNameIsPostfix=True)
         EchoOutputFile(OutputFileName)
         InputFileName=GetLine(keyPattern)

   # one file to one file
   elif One2One : 
      InputFileName=opt.InFile
      EchoInputFile(InputFileName)
      OutputFileName=my_sp.once(InputFileName)
      EchoOutputFile(OutputFileName)

   #nothing
   else :
      print "Nothing to do"

   #if sp_glob.verbose : print 'Out[0,0,88,0]=',my_sp.COSM[0,0,88,0], type(my_sp.COSM[0,0,88,0]), repr(my_sp.COSM[0,0,88,0]),my_sp.COSM[:,:,88,0]

   if opt.bm : sp_bm.bm_close()



if __name__ == "__main__":
   main()

