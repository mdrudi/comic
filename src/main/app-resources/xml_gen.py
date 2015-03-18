def sPar(parent,id,txt,title=None,abstract=None,scope=None) :
   parameter=ET.SubElement(parent,'parameter')
   parameter.set('id',id)
   if title is not None : parameter.set('title',title)
   if abstract is not None : parameter.set('abstract',abstract)
   if scope is not None : parameter.set('scope',scope)
   parameter.text=txt
   parameter.tail='\n'

def sNodeMonth(workflow,y,m) :
   strYYYYMM=str(y)+m
   node=ET.SubElement(workflow,'node')
   node.set('id','node_t_'+strYYYYMM)
   node.text='\n'
   node.tail='\n'

   ET.SubElement(node,'job').set('id','jt_t')

   sources=ET.SubElement(node,'sources')
   sources.text='\n'
   sources.tail='\n'

   source=ET.SubElement(sources,'source')
   source.set('refid','wf:node')
   source.text='node_v'
   source.tail='\n'

   parameters=ET.SubElement(node,'parameters')
   parameters.text='\n'
   parameters.tail='\n'

   sPar(parameters,'OutFile','last'+strYYYYMM+'.nc')
   sPar(parameters,'iKey','/'+strYYYYMM+'|^'+strYYYYMM)



import xml.etree.ElementTree as ET
import sys
startYear=int(sys.argv[1])
endYear=int(sys.argv[2])
endMonth=int(sys.argv[3])


application=ET.Element('application')
application.set('xmlns:xsi',"http://www.w3.org/2001/XMLSchema-instance")
application.set('xmlns:xsd',"http://www.w3.org/2001/XMLSchema")
application.set('id',"wp6_app_id")
application.text='\n'

jobTemplates=ET.SubElement(application,'jobTemplates')
jobTemplates.text='\n'
jobTemplates.tail='\n'

# jt_v 

jobTemplate=ET.SubElement(jobTemplates,'jobTemplate')
jobTemplate.set('id',"jt_v")
jobTemplate.text='\n'
jobTemplate.tail='\n'

streamingExecutable=ET.SubElement(jobTemplate,'streamingExecutable')
streamingExecutable.text='/application/jt_vto/run.py'
streamingExecutable.tail='\n'

defaultParameters=ET.SubElement(jobTemplate,'defaultParameters')
defaultParameters.text='\n'
defaultParameters.tail='\n'

sPar(defaultParameters,'InFile','list')
#sPar(defaultParameters,'iKey','')
sPar(defaultParameters,'Var','votemper',title="Parameter",abstract="Parameter", scope="runtime")
sPar(defaultParameters,'LonLat','',title="WorkingArea",abstract="default None", scope="runtime")
#sPar(defaultParameters,'LonLat','')
sPar(defaultParameters,'OutFile','.out.nc')
#sPar(defaultParameters,'oat','')
sPar(defaultParameters,'OutLayer','[0,10,50,100,500,1000,2000]',title="DepthLayers",abstract="default [0,10,50,100,500,1000,2000]",scope="runtime")
#sPar(defaultParameters,'oao','')
#sPar(defaultParameters,'otc','')
sPar(defaultParameters,'bm','True')
#sPar(defaultParameters,'s','False')
sPar(defaultParameters,'iClean','True')
#sPar(defaultParameters,'iKey','',title="Key",abstract="default None",scope="runtime") # does not work properly : better if the input files are exactly what you want to process

# jt_g

jobTemplate=ET.SubElement(jobTemplates,'jobTemplate')
jobTemplate.set('id',"jt_g")
jobTemplate.text='\n'
jobTemplate.tail='\n'

streamingExecutable=ET.SubElement(jobTemplate,'streamingExecutable')
streamingExecutable.text='/application/jt_vto/node_g.py'
streamingExecutable.tail='\n'

defaultParameters=ET.SubElement(jobTemplate,'defaultParameters')
defaultParameters.text='\n'
defaultParameters.tail='\n'

sPar(defaultParameters,'iKey','.nc$')

defaultJobconf=ET.SubElement(jobTemplate,'defaultJobconf')
defaultJobconf.text='\n'
defaultJobconf.tail='\n'

property=ET.SubElement(defaultJobconf,'property')
property.set('id','ciop.job.max.tasks')
property.text='1'
property.tail='\n'

# jt_t

jobTemplate=ET.SubElement(jobTemplates,'jobTemplate')
jobTemplate.set('id',"jt_t")
jobTemplate.text='\n'
jobTemplate.tail='\n'

streamingExecutable=ET.SubElement(jobTemplate,'streamingExecutable')
streamingExecutable.text='/application/jt_vto/run.py'
streamingExecutable.tail='\n'

defaultParameters=ET.SubElement(jobTemplate,'defaultParameters')
defaultParameters.text='\n'
defaultParameters.tail='\n'

sPar(defaultParameters,'InFile','list')
#sPar(defaultParameters,'iKey','/lastcomic|^lastcomic')
sPar(defaultParameters,'iKey','\.txt$')
sPar(defaultParameters,'Var','votemper')
#sPar(defaultParameters,'LonLat','')
sPar(defaultParameters,'OutFile','.out.nc')
sPar(defaultParameters,'oat','True')
#sPar(defaultParameters,'OutLayer','')
#sPar(defaultParameters,'oao','')
#sPar(defaultParameters,'otc','')
sPar(defaultParameters,'bm','True')
sPar(defaultParameters,'s','True')
sPar(defaultParameters,'iClean','True')


defaultJobconf=ET.SubElement(jobTemplate,'defaultJobconf')
defaultJobconf.text='\n'
defaultJobconf.tail='\n'

#myRange=range(startYear,endYear+1)

property=ET.SubElement(defaultJobconf,'property')
property.set('id','ciop.job.max.tasks')
property.text=str((endYear-startYear)*12+endMonth)
property.tail='\n'

#jt_o

jobTemplate=ET.SubElement(jobTemplates,'jobTemplate')
jobTemplate.set('id',"jt_o")
jobTemplate.text='\n'
jobTemplate.tail='\n'

streamingExecutable=ET.SubElement(jobTemplate,'streamingExecutable')
streamingExecutable.text='/application/jt_vto/run.py'
streamingExecutable.tail='\n'

defaultParameters=ET.SubElement(jobTemplate,'defaultParameters')
defaultParameters.text='\n'
defaultParameters.tail='\n'

sPar(defaultParameters,'InFile','list')
#sPar(defaultParameters,'iKey','/lastcomic6|^lastcomic6')
sPar(defaultParameters,'Var','votemper')
#sPar(defaultParameters,'LonLat','')
#sPar(defaultParameters,'OutFile','out.nc')
#sPar(defaultParameters,'oat','')
#sPar(defaultParameters,'OutLayer','')
sPar(defaultParameters,'oao','True')
sPar(defaultParameters,'otc','True')
sPar(defaultParameters,'bm','True')
#sPar(defaultParameters,'s','True')
sPar(defaultParameters,'iClean','True')

defaultJobconf=ET.SubElement(jobTemplate,'defaultJobconf')
defaultJobconf.text='\n'
defaultJobconf.tail='\n'

property=ET.SubElement(defaultJobconf,'property')
property.set('id','ciop.job.max.tasks')
property.text='1'
property.tail='\n'

# workflow

workflow=ET.SubElement(application,'workflow')
workflow.set('id','wp6_wf_id')
workflow.set('title','WP6 workflow '+str(startYear)+' 01 '+str(endYear)+' '+str(endMonth))
workflow.set('abstract','Toolbox parameters')
workflow.text='\n'
workflow.tail='\n'

workflowVersion=ET.SubElement(workflow,'workflowVersion')
workflowVersion.text='1.0'
workflowVersion.tail='\n'

# node_v

node=ET.SubElement(workflow,'node')
node.set('id','node_v')
node.text='\n'
node.tail='\n'

ET.SubElement(node,'job').set('id','jt_v')

sources=ET.SubElement(node,'sources')
sources.text='\n'
sources.tail='\n'

source=ET.SubElement(sources,'source')
source.set('refid','file:urls')
source.text='/application/inputfiles'
source.tail='\n'

parameters=ET.SubElement(node,'parameters')
parameters.text='\n'
parameters.tail='\n'

# node_g_m

node=ET.SubElement(workflow,'node')
node.set('id','node_g_m')
node.text='\n'
node.tail='\n'

ET.SubElement(node,'job').set('id','jt_g')

sources=ET.SubElement(node,'sources')
sources.text='\n'
sources.tail='\n'

source=ET.SubElement(sources,'source')
source.set('refid','wf:node')
source.text='node_v'
source.tail='\n'

parameters=ET.SubElement(node,'parameters')
parameters.text='\n'
parameters.tail='\n'

sPar(parameters,'GroupRange','6')

# node_t_m

#myRange=range(startYear,endYear+1)

#for i in myRange :
#   for m in ('01','02','03','04','05','06','07','08','09','10','11','12') :
#      sNodeMonth(workflow,i,m)
#      if i == endYear and m == endMonth : break

node=ET.SubElement(workflow,'node')
node.set('id','node_t_m')
node.text='\n'
node.tail='\n'

ET.SubElement(node,'job').set('id','jt_t')

sources=ET.SubElement(node,'sources')
sources.text='\n'
sources.tail='\n'

source=ET.SubElement(sources,'source')
source.set('refid','wf:node')
source.text='node_g_m'
source.tail='\n'

parameters=ET.SubElement(node,'parameters')
parameters.text='\n'
parameters.tail='\n'

#sPar(parameters,'OutFile','last'+strYYYYMM+'.nc')
#sPar(parameters,'iKey','/'+strYYYYMM+'|^'+strYYYYMM)

# node_g_a

node=ET.SubElement(workflow,'node')
node.set('id','node_g_a')
node.text='\n'
node.tail='\n'

ET.SubElement(node,'job').set('id','jt_g')

sources=ET.SubElement(node,'sources')
sources.text='\n'
sources.tail='\n'

source=ET.SubElement(sources,'source')
source.set('refid','wf:node')
source.text='node_t_m'
source.tail='\n'

parameters=ET.SubElement(node,'parameters')
parameters.text='\n'
parameters.tail='\n'

sPar(parameters,'GroupRange','4')

# node_o_m 

node=ET.SubElement(workflow,'node')
node.set('id','node_o_m')
node.text='\n'
node.tail='\n'

ET.SubElement(node,'job').set('id','jt_o')

sources=ET.SubElement(node,'sources')
sources.text='\n'
sources.tail='\n'

#for y in myRange :
#   for m in ('01','02','03','04','05','06','07','08','09','10','11','12') :
#      source=ET.SubElement(sources,'source')
#      source.set('refid','wf:node')
#      source.text='node_t_'+str(y)+m
#      source.tail='\n'
#      if y == endYear and m == endMonth : break

source=ET.SubElement(sources,'source')
source.set('refid','wf:node')
source.text='node_t_m'
source.tail='\n'

parameters=ET.SubElement(node,'parameters')
parameters.text='\n'
parameters.tail='\n'

sPar(parameters,'iKey','\.nc$')
sPar(parameters,'OutFile','out6.nc')

#node_t_a

node=ET.SubElement(workflow,'node')
node.set('id','node_t_a')
node.text='\n'
node.tail='\n'

ET.SubElement(node,'job').set('id','jt_t')

sources=ET.SubElement(node,'sources')
sources.text='\n'
sources.tail='\n'

source=ET.SubElement(sources,'source')
source.set('refid','wf:node')
source.text='node_g_a'
source.tail='\n'

parameters=ET.SubElement(node,'parameters')
parameters.text='\n'
parameters.tail='\n'

#node_o_a

node=ET.SubElement(workflow,'node')
node.set('id','node_o_a')
node.text='\n'
node.tail='\n'

ET.SubElement(node,'job').set('id','jt_o')

sources=ET.SubElement(node,'sources')
sources.text='\n'
sources.tail='\n'

#for y in myRange :
#   for m in ('01','02','03','04','05','06','07','08','09','10','11','12') :
#      source=ET.SubElement(sources,'source')
#      source.set('refid','wf:node')
#      source.text='node_t_'+str(y)+m
#      source.tail='\n'
#      if y == endYear and m == endMonth : break

source=ET.SubElement(sources,'source')
source.set('refid','wf:node')
source.text='node_o_m'
source.tail='\n'

source=ET.SubElement(sources,'source')
source.set('refid','wf:node')
source.text='node_t_a'
source.tail='\n'

parameters=ET.SubElement(node,'parameters')
parameters.text='\n'
parameters.tail='\n'

sPar(parameters,'iKey','mapcomic4(.*)(\.nc$)')
sPar(parameters,'OutFile','out4.nc')

#ET.dump(application)
print ET.tostring(application)

