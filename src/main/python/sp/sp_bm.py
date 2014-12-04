BM_INIT=1
BM_READ=2
BM_WRITE=3
BM_COMPUTE=4
#BM_ID=5
#BM_OD=6
BM_BM=7
BM_WRAP=8
t_last=0
#t_init=0   REMOVE ASAP
#t_read=0
#t_compute=0
#t_write=0
bminfo=0

def bm_setup() :
   import time
   global t_last
   #global t_init   REMOVE ASAP
   #global t_read
   #global t_compute
   #global t_write
   global bminfo
   t_last=time.time()
   t_init=0
   t_read=0
   t_compute=0
   t_write=0
   bminfo=dict(t_init=0,t_read=0,t_compute=0,t_write=0,t_bm=0,t_wrap=0,in_byte=0,in_point=0,in_spoint=0,out_byte=0,out_point=0,out_spoint=0,p_max_mem=0)

def bm_update(type,data=None) :
   import time
   import resource
   global BM_INIT
   global BM_READ
   global BM_WRITE
   global BM_COMPUTE
   global BM_WRAP
#   global BM_ID
#   global BM_OD
   global bminfo
   global t_last
   mm=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
   if mm > bminfo['p_max_mem'] : bminfo['p_max_mem']=mm
   t_new=time.time()
   delta=round((t_new-t_last)*1000)
   #t_last=t_new
   if type == BM_INIT : 
      #global t_init
      bminfo['t_init']+=delta
   if type == BM_WRAP :
      bminfo['t_wrap']+=delta
   elif type == BM_READ :
      #global t_read
      bminfo['t_read']+=delta
      if data is not None :
         t_last=t_new
         bminfo['in_byte']+=data.nbytes
         bminfo['in_point']+=data.size
         bminfo['in_spoint']+=data.count()
         t_new=time.time()
         delta=round((t_new-t_last)*1000)
         bminfo['t_bm']+=delta
   elif type == BM_COMPUTE :
      #global t_compute
      bminfo['t_compute']+=delta
   elif type == BM_WRITE :
      #global t_write
      bminfo['t_write']+=delta
      if data is not None :
         t_last=t_new
         bminfo['out_byte']+=data.nbytes
         bminfo['out_point']+=data.size
         bminfo['out_spoint']+=data.count()
         t_new=time.time()
         delta=round((t_new-t_last)*1000)
         bminfo['t_bm']+=delta
   t_last=t_new

#   elif type == BM_ID :
#      bminfo['in_byte']+=data.nbytes
#      bminfo['in_point']+=data.size
#      bminfo['in_spoint']+=data.count()
#      bminfo['t_bm']+=delta
#   elif type == BM_OD :
#      bminfo['out_byte']+=data.nbytes
#      bminfo['out_point']+=data.size
#      bminfo['out_spoint']+=data.count()
#      bminfo['t_bm']+=delta


def bm_close() :
   #global t_init
   #global t_read
   #global t_compute
   #global t_write
   global bminfo
   tot=bminfo['t_init']+bminfo['t_read']+bminfo['t_compute']+bminfo['t_write']+bminfo['t_bm']+bminfo['t_wrap']
   tot100=tot/100

   print "\nbm---------------"

   print "\nInput Data"
   print "|  byte in memory  : ", bminfo['in_byte']
   print "|  # grid point    : ", bminfo['in_point']
   print "`  # sea point     : ", bminfo['in_spoint']

   print "\nOutput Data"
   print "|  byte in memory  : ", bminfo['out_byte']
   print "|  # grid point    : ", bminfo['out_point']
   print "`  # sea point     : ", bminfo['out_spoint']

   print "\nMax Memory         : ", bminfo['p_max_mem']*1024

   print '\nInit         : (ms)',int(bminfo['t_init']),'-',int(round(bminfo['t_init']/tot100)),'%'
   print 'i/o read     : (ms)',int(bminfo['t_read']),'-',int(round(bminfo['t_read']/tot100)),'%'
   print 'computation  : (ms)',int(bminfo['t_compute']),'-',int(round(bminfo['t_compute']/tot100)),'%'
   print 'i/o write    : (ms)',int(bminfo['t_write']),'-',int(round(bminfo['t_write']/tot100)),'%'
   print 'benchmarking : (ms)',int(bminfo['t_bm']),'-',int(round( bminfo['t_bm'] /tot100)),'%'
   print 'wrap         : (ms)',int(bminfo['t_wrap']),'-',int(round( bminfo['t_wrap'] /tot100)),'%'
   print 'tot          :  (s)',tot/1000

   #bminfo['t_init']=t_init
   #bminfo['t_read']=t_read
   #bminfo['t_compute']=t_compute
   #bminfo['t_write']=t_write

   #print bminfo
   import json
   json.dump(bminfo,open('bm.txt','w'))


