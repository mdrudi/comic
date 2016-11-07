import xml.etree.ElementTree as ET


def sPar(parent, id, txt, title=None, abstract=None, scope=None):
    parameter = ET.SubElement(parent, 'parameter')
    parameter.set('id', id)
    if title is not None:
        parameter.set('title', title)
    if abstract is not None:
        parameter.set('abstract', abstract)
    if scope is not None:
        parameter.set('scope', scope)
    parameter.text = txt
    parameter.tail = '\n'


application = ET.Element('application')
application.set('xmlns:xsi', "http://www.w3.org/2001/XMLSchema-instance")
application.set('xmlns:xsd', "http://www.w3.org/2001/XMLSchema")
application.set('id', "wp6_app_id")
application.text = '\n'

jobTemplates = ET.SubElement(application, 'jobTemplates')
jobTemplates.text = '\n'
jobTemplates.tail = '\n'

# annual climatology template

jobTemplate = ET.SubElement(jobTemplates, 'jobTemplate')
jobTemplate.set('id', "jt_an_clim")
jobTemplate.text = '\n'
jobTemplate.tail = '\n'

streamingExecutable = ET.SubElement(jobTemplate, 'streamingExecutable')
streamingExecutable.text = '/application/jt_vto/run.py'
streamingExecutable.tail = '\n'

defaultParameters = ET.SubElement(jobTemplate, 'defaultParameters')
defaultParameters.text = '\n'
defaultParameters.tail = '\n'

sPar(defaultParameters, 'InFile', 'list')
sPar(defaultParameters, 'Var', '', title="Variable", abstract="Variable", scope="runtime")
sPar(defaultParameters, 'oac', 'True')
sPar(defaultParameters, 'bm', 'True')
sPar(defaultParameters, 'iClean', 'False')

defaultJobconf = ET.SubElement(jobTemplate, 'defaultJobconf')
defaultJobconf.text = '\n'
defaultJobconf.tail = '\n'

property = ET.SubElement(defaultJobconf, 'property')
property.set('id', 'ciop.job.max.tasks')
property.text = '1'
property.tail = '\n'

# basin mean timeseries template

jobTemplate = ET.SubElement(jobTemplates, 'jobTemplate')
jobTemplate.set('id', "jt_basin_m_ts")
jobTemplate.text = '\n'
jobTemplate.tail = '\n'

streamingExecutable = ET.SubElement(jobTemplate, 'streamingExecutable')
streamingExecutable.text = '/application/jt_vto/run.py'
streamingExecutable.tail = '\n'

defaultParameters = ET.SubElement(jobTemplate, 'defaultParameters')
defaultParameters.text = '\n'
defaultParameters.tail = '\n'

sPar(defaultParameters, 'InFile', 'list')
sPar(defaultParameters, 'Var', '', title="Variable", abstract="Variable", scope="runtime")
sPar(defaultParameters, 'oao', 'True')
sPar(defaultParameters, 'otc', 'True')
sPar(defaultParameters, 'bm', 'True')
sPar(defaultParameters, 'iClean', 'False')

defaultJobconf = ET.SubElement(jobTemplate, 'defaultJobconf')
defaultJobconf.text = '\n'
defaultJobconf.tail = '\n'

property = ET.SubElement(defaultJobconf, 'property')
property.set('id', 'ciop.job.max.tasks')
property.text = '1'
property.tail = '\n'

# annual climatology and basin mean timeseries workflow

workflow = ET.SubElement(application, 'workflow')
workflow.set('id', 'wp6_wf_id')
workflow.set('title', 'WP6 annual climatology and basin mean timeseries workflow')
workflow.set('abstract', 'Toolbox parameters')
workflow.text = '\n'
workflow.tail = '\n'

workflowVersion = ET.SubElement(workflow, 'workflowVersion')
workflowVersion.text = '1.0'
workflowVersion.tail = '\n'

# compute annual climatology

node = ET.SubElement(workflow, 'node')
node.set('id', 'an_clim')
node.text = '\n'
node.tail = '\n'

ET.SubElement(node, 'job').set('id', 'jt_an_clim')

sources = ET.SubElement(node, 'sources')
sources.text = '\n'
sources.tail = '\n'

source = ET.SubElement(sources, 'source')
source.set('refid', 'file:urls')
source.text = '/application/inputfiles'
source.tail = '\n'

parameters = ET.SubElement(node, 'parameters')
parameters.text = '\n'
parameters.tail = '\n'

sPar(parameters, 'iKey', 'mapcomic2(.*)(\.nc$)')
sPar(parameters, 'OutFile', 'out_m_12.nc')

# compute monthly basin mean timeseries

node = ET.SubElement(workflow, 'node')
node.set('id', 'basin_m_ts')
node.text = '\n'
node.tail = '\n'

ET.SubElement(node, 'job').set('id', 'jt_basin_m_ts')

sources = ET.SubElement(node, 'sources')
sources.text = '\n'
sources.tail = '\n'

source = ET.SubElement(sources, 'source')
source.set('refid', 'file:urls')
source.text = '/application/inputfiles'
source.tail = '\n'

source = ET.SubElement(sources, 'source')
source.set('refid', 'wf:node')
source.text = 'an_clim'
source.tail = '\n'

parameters = ET.SubElement(node, 'parameters')
parameters.text = '\n'
parameters.tail = '\n'

sPar(parameters, 'iKey', 'mapcomic2(.*)(\.nc$)')
sPar(parameters, 'OutFile', 'out_ts_12.nc')

# ET.dump(application)
print ET.tostring(application)