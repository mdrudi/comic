#!/usr/bin/python

from ionc import ReadFile, WriteFile
import sp_bm


class sp :
   def __init__(self,InputVariableName,OutFileName,LonLat=None,OutputLayer=None,bm=False,SpeedUp=False,OutLonLat=None,TimeRange=None,RemoveInput=False) :

      self.OutApp=None

      #par to read data
      self.InputVariableName=InputVariableName
      self.LonLat=LonLat 
      #self.Lat=Lat
      self.LonMinMax=None
      self.LatMinMax=None
      if self.LonLat is not None :
         self.LonMinMax=[0,0]
         self.LatMinMax=[0,0]
         self.LonMinMax[0]=self.LonLat[0][0][0]
         self.LonMinMax[1]=self.LonLat[0][0][1]
         self.LatMinMax[0]=self.LonLat[0][1][0]
         self.LatMinMax[1]=self.LonLat[0][1][1]
         for Region in self.LonLat :
            LonRange=Region[0]
            LatRange=Region[1]
            if self.LonMinMax[0]>LonRange[0] : self.LonMinMax[0]=LonRange[0]
            if self.LonMinMax[1]<LonRange[1] : self.LonMinMax[1]=LonRange[1]
            if self.LatMinMax[0]>LatRange[0] : self.LatMinMax[0]=LatRange[0]
            if self.LatMinMax[1]<LatRange[1] : self.LatMinMax[1]=LatRange[1]

      #par to elaborate and output data
      self.OutputLayer=OutputLayer
      self.OutFileName=OutFileName
      self.OutLonLat=OutLonLat
      self.TimeRange=TimeRange

      #behaviour flags
      self.bm=bm
      self.SpeedUp=SpeedUp
      #self.sList=sList
      self.CatList=list()
      self.RemoveInput=RemoveInput

   def once(self,InputFileName,OutFileNameIsPostfix=False) :
      print 'WARNING 5 : possible improvement if data to read is reduced to the min size'
      #print self.LonMinMax,self.LatMinMax

      InApp=ReadFile(InputFileName,self.InputVariableName,self.LonMinMax,self.LatMinMax,self.OutputLayer,self.RemoveInput)
      #print InApp.COSM.size
      if self.bm : sp_bm.bm_update(sp_bm.BM_READ,InApp.COSM)

      self.OutApp=InApp
      if self.LonLat is not None : self.OutApp.mask_out_of(self.LonLat)
      if self.OutputLayer is not None or self.OutLonLat is not None :
         self.OutApp.operator_s(self.OutputLayer,self.OutLonLat)
      if self.bm : sp_bm.bm_update(sp_bm.BM_COMPUTE)

      if OutFileNameIsPostfix :
         OutFileName=InputFileName+self.OutFileName
      else :
         OutFileName=self.OutFileName
      WriteFile(self.OutApp,OutFileName)
      if self.bm : sp_bm.bm_update(sp_bm.BM_WRITE,self.OutApp.COSM)

      self.OutApp=None
      return OutFileName

   def loop_go(self,InputFileName) :
      print 'WARNING 6 : possible improvement if data to read is reduced'
      #print self.LonMinMax,self.LatMinMax

      InApp=ReadFile(InputFileName,self.InputVariableName,self.LonMinMax,self.LatMinMax,self.OutputLayer,self.RemoveInput)
      if self.bm : sp_bm.bm_update(sp_bm.BM_READ,InApp.COSM)

      # TIMESERIES WITH OR WITHOUT LAYERS
      if self.OutApp is None :
         self.OutApp=InApp
         if self.LonLat is not None : self.OutApp.mask_out_of(self.LonLat)
         if not ( self.SpeedUp and (self.OutputLayer is not None or self.OutLonLat is not None ) ) :
            self.OutApp.operator_s(self.OutputLayer,self.OutLonLat)
         if self.TimeRange is not None :
            self.OutApp.set_weight(self.TimeRange)
      else :
         #import numpy
         #print type(self.TimeAverage)
         if self.TimeRange is not None :   #ture = TimeRange is a time range or an empty time range ; false = TimeRange is None
            self.OutApp.operator_tAdd(InApp,TimeAverage=True)
         else :
            if self.LonLat is not None : InApp.mask_out_of(self.LonLat)
            #if self.OutApp.TimeCells[-1] == InApp.TimeCells[0] or self.OutApp.TimeCells[0] == InApp.TimeCells[1] :
            if self.OutApp.IsAdiacent(InApp) :
               self.OutApp.operator_tAdd(InApp)     #,self.TimeAverage)
            else :
               self.CatList.append(InApp)
               print 'WARNING 15 : not able to handle this case now : concatenation postponed'
      
#      print 'TGH :',self.OutApp.TimeCells,InApp.TimeCells
#      if self.TimeAverage : 
#         self.OutApp.operator_tAdd(InApp,self.TimeAverage)
#      else :
#         #print 'TGH :',self.OutApp.TimeCells,InApp.TimeCells
#         if self.OutApp.TimeCells is None :
#            self.OutApp.operator_tAdd(InApp,self.TimeAverage)
#         elif self.OutApp.TimeCells[-1] == InApp.TimeCells[0] or self.OutApp.TimeCells[0] == InApp.TimeCells[1] :
#            self.OutApp.operator_tAdd(InApp,self.TimeAverage)
#         else :
#            print 'WARNING 15 : not able to handle this case now : concatenation postponed'
#            self.CatList.append(InApp)
      if self.bm : sp_bm.bm_update(sp_bm.BM_COMPUTE)


   def loop_close(self) :
      if self.TimeRange is not None :   #ture = TimeRange is a time range or an empty time range ; false = TimeRange is None
         self.OutApp.operator_tClose()
      else :
         maxi=len(self.CatList)
         while len(self.CatList) != 0 and maxi != 0 :
            maxi=maxi-1
            for i in range(len(self.CatList)) :
               InApp=self.CatList.pop(0)
            #for InApp in self.CatList :
               #if self.OutApp.TimeCells[-1] == InApp.TimeCells[0] or self.OutApp.TimeCells[0] == InApp.TimeCells[1] : 
               if self.OutApp.IsAdiacent(InApp) :
                  self.OutApp.operator_tAdd(InApp)    #,self.TimeAverage)
               else :
                  self.CatList.append(InApp)
      if len(self.CatList) != 0 : print 'ERROR 1 : wrong input'
      print 'WARNING 1: something to improve...'  # in ch ordine tclose e operator_s
      if self.SpeedUp and (self.OutputLayer is not None or self.OutLonLat is not None ) :
         self.OutApp.operator_s(self.OutputLayer,self.OutLonLat)
      #print 'XXX lc',self.OutApp.COSM.shape
      if self.bm : sp_bm.bm_update(sp_bm.BM_COMPUTE)
      WriteFile(self.OutApp,self.OutFileName)
      if self.bm : sp_bm.bm_update(sp_bm.BM_WRITE,self.OutApp.COSM)
      self.OutApp=None
      return self.OutFileName



