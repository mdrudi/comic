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

# vertical interpolation template

jobTemplate = ET.SubElement(jobTemplates, 'jobTemplate')
jobTemplate.set('id', "jt_v_interp")
jobTemplate.text = '\n'
jobTemplate.tail = '\n'

streamingExecutable = ET.SubElement(jobTemplate, 'streamingExecutable')
streamingExecutable.text = '/application/jt_vto/run.py'
streamingExecutable.tail = '\n'

defaultParameters = ET.SubElement(jobTemplate, 'defaultParameters')
defaultParameters.text = '\n'
defaultParameters.tail = '\n'

sPar(defaultParameters, 'InFile', 'list')
sPar(defaultParameters, 'Var', '', title="Working Parameter", abstract="Example: votemper", scope="runtime")
sPar(defaultParameters, 'OutFile', '.out.nc')
sPar(defaultParameters, 'OutLayer', '[0,10,50,100,500,1000,2000]', title="DepthLayers",
     abstract="default [0,10,50,100,500,1000,2000]", scope="runtime")
sPar(defaultParameters, 'bm', 'True')
sPar(defaultParameters, 'iClean', 'True')

# node_g input files split template

jobTemplate = ET.SubElement(jobTemplates, 'jobTemplate')
jobTemplate.set('id', "jt_split")
jobTemplate.text = '\n'
jobTemplate.tail = '\n'

streamingExecutable = ET.SubElement(jobTemplate, 'streamingExecutable')
streamingExecutable.text = '/application/jt_vto/node_g.py'
streamingExecutable.tail = '\n'

defaultParameters = ET.SubElement(jobTemplate, 'defaultParameters')
defaultParameters.text = '\n'
defaultParameters.tail = '\n'

sPar(defaultParameters, 'iKey', '.nc$|.gz$')
sPar(defaultParameters, 'oKey', 'None')

defaultJobconf = ET.SubElement(jobTemplate, 'defaultJobconf')
defaultJobconf.text = '\n'
defaultJobconf.tail = '\n'

property = ET.SubElement(defaultJobconf, 'property')
property.set('id', 'ciop.job.max.tasks')
property.text = '1'
property.tail = '\n'

# time average template

jobTemplate = ET.SubElement(jobTemplates, 'jobTemplate')
jobTemplate.set('id', "jt_t_avg")
jobTemplate.text = '\n'
jobTemplate.tail = '\n'

streamingExecutable = ET.SubElement(jobTemplate, 'streamingExecutable')
streamingExecutable.text = '/application/jt_vto/run.py'
streamingExecutable.tail = '\n'

defaultParameters = ET.SubElement(jobTemplate, 'defaultParameters')
defaultParameters.text = '\n'
defaultParameters.tail = '\n'

sPar(defaultParameters, 'InFile', 'list')
sPar(defaultParameters, 'iKey', '\.txt$')
sPar(defaultParameters, 'Var', '', title="Working Parameter", abstract="Example: votemper", scope="runtime")
sPar(defaultParameters, 'LonLat', 'None', title="WorkingArea", abstract="default None", scope="runtime")
sPar(defaultParameters, 'OutFile', '.out.nc')
sPar(defaultParameters, 'oat', '[]')
sPar(defaultParameters,  'bm', 'True')
sPar(defaultParameters, 's', 'True')
sPar(defaultParameters, 'iClean', 'True')

# monthly mean workflow

workflow = ET.SubElement(application, 'workflow')
workflow.set('id', 'wp6_wf_id')
workflow.set('title', 'WP6 monthly mean workflow')
workflow.set('abstract', 'Toolbox parameters')
workflow.text = '\n'
workflow.tail = '\n'

workflowVersion = ET.SubElement(workflow, 'workflowVersion')
workflowVersion.text = '1.0'
workflowVersion.tail = '\n'

# compute vertical interpolation

node = ET.SubElement(workflow, 'node')
node.set('id', 'v_interp')
node.text = '\n'
node.tail = '\n'

ET.SubElement(node, 'job').set('id', 'jt_v_interp')

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

# compute monthly mean calculus node_g split

node = ET.SubElement(workflow, 'node')
node.set('id', 'mm_input_split')
node.text = '\n'
node.tail = '\n'

ET.SubElement(node, 'job').set('id', 'jt_split')

sources = ET.SubElement(node, 'sources')
sources.text = '\n'
sources.tail = '\n'

source = ET.SubElement(sources, 'source')
source.set('refid', 'wf:node')
source.text = 'v_interp'
source.tail = '\n'

parameters = ET.SubElement(node, 'parameters')
parameters.text = '\n'
parameters.tail = '\n'

sPar(parameters, 'GroupRange', '6')

# compute monthly mean maps

node = ET.SubElement(workflow, 'node')
node.set('id', 'mm_calc')
node.text = '\n'
node.tail = '\n'

ET.SubElement(node, 'job').set('id', 'jt_t_avg')

sources = ET.SubElement(node, 'sources')
sources.text = '\n'
sources.tail = '\n'

source = ET.SubElement(sources, 'source')
source.set('refid', 'wf:node')
source.text = 'mm_input_split'
source.tail = '\n'

parameters = ET.SubElement(node, 'parameters')
parameters.text = '\n'
parameters.tail = '\n'

sPar(parameters, 'oat', '["i6"]')
sPar(parameters, 'AttrStr', '{"votemper": {"long_name": "Temperature", "units": "degC"},'
                            '"vosaline": {"long_name": "Salinity", "units": "1e-3"},'
                            '"vozocrtx": {"long_name": "Zonal Velocity", "units": "m/s"},'
                            '"vomecrty": {"long_name": "Meridional Velocity", "units": "m/s"},'
                            '"sozotaux": {"long_name": "Zonal Wind Stress", "units": "N/m2"},'
                            '"sometauy": {"long_name": "Meridional Wind Stress", "units": "N/m2"},'
                            '"global":{"title": "monthly mean map","source": "copernicus med mfc toolbox",'
                            '"institution": "MELODIES WP6 ACS INGV"}}')

# ET.dump(application)
print ET.tostring(application)