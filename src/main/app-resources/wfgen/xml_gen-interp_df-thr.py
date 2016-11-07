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

# derived field calculator template

jobTemplate = ET.SubElement(jobTemplates, 'jobTemplate')
jobTemplate.set('id', "jt_df_calc")
jobTemplate.text = '\n'
jobTemplate.tail = '\n'

streamingExecutable = ET.SubElement(jobTemplate, 'streamingExecutable')
streamingExecutable.text = '/application/jt_vto/run.py'
streamingExecutable.tail = '\n'

defaultParameters = ET.SubElement(jobTemplate, 'defaultParameters')
defaultParameters.text = '\n'
defaultParameters.tail = '\n'

sPar(defaultParameters, 'InFile', 'list')
sPar(defaultParameters, 'OutField', '', title="Output derived field", abstract="Example: votkeavt", scope="runtime")
sPar(defaultParameters, 'Var', '', title="Output Variable", abstract="Must be the same as OutField", scope="runtime")
sPar(defaultParameters, 'LonLat', 'None', title="WorkingArea", abstract="default None", scope="runtime")
sPar(defaultParameters, 'OutFile', '.out.nc')
sPar(defaultParameters, 'OutLayer', '[0,10,50,100,500,1000,2000]', title="DepthLayers",
     abstract="default [0,10,50,100,500,1000,2000]", scope="runtime")
sPar(defaultParameters, 'bm', 'True')
sPar(defaultParameters, 'iClean', 'True')

# variable threshold template

jobTemplate = ET.SubElement(jobTemplates, 'jobTemplate')
jobTemplate.set('id', "jt_threshold")
jobTemplate.text = '\n'
jobTemplate.tail = '\n'

streamingExecutable = ET.SubElement(jobTemplate, 'streamingExecutable')
streamingExecutable.text = '/application/jt_vto/threshold.py'
streamingExecutable.tail = '\n'

defaultParameters = ET.SubElement(jobTemplate, 'defaultParameters')
defaultParameters.text = '\n'
defaultParameters.tail = '\n'

sPar(defaultParameters, 'iKey', '.nc$|.gz$')
sPar(defaultParameters, 'Var', '', title="Output Variable", abstract="Must be the same as OutField", scope="runtime")
sPar(defaultParameters, 'Threshold', '', title="Threshold scalar (float)", abstract="Example: 3e-06", scope="runtime")

defaultJobconf = ET.SubElement(jobTemplate, 'defaultJobconf')
defaultJobconf.text = '\n'
defaultJobconf.tail = '\n'

# derived field threshold workflow

workflow = ET.SubElement(application, 'workflow')
workflow.set('id', 'wp6_wf_id')
workflow.set('title', 'WP6 derived field threshold workflow')
workflow.set('abstract', 'Toolbox parameters')
workflow.text = '\n'
workflow.tail = '\n'

workflowVersion = ET.SubElement(workflow, 'workflowVersion')
workflowVersion.text = '1.0'
workflowVersion.tail = '\n'

# compute derived field node_g split

node = ET.SubElement(workflow, 'node')
node.set('id', 'df_input_split')
node.text = '\n'
node.tail = '\n'

ET.SubElement(node, 'job').set('id', 'jt_split')

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

sPar(parameters, 'GroupRange', '66')

# compute derived field

node = ET.SubElement(workflow, 'node')
node.set('id', 'df_calc')
node.text = '\n'
node.tail = '\n'

ET.SubElement(node, 'job').set('id', 'jt_df_calc')

sources = ET.SubElement(node, 'sources')
sources.text = '\n'
sources.tail = '\n'

source = ET.SubElement(sources, 'source')
source.set('refid', 'wf:node')
source.text = 'df_input_split'
source.tail = '\n'

parameters = ET.SubElement(node, 'parameters')
parameters.text = '\n'
parameters.tail = '\n'

sPar(parameters, 'iKey', '\.txt$')
sPar(parameters, 'AttrStr', '{"vodnsity": {"long_name": "Sea Water Density", "units": "Kg/m3"},'
                            '"vokenerg": {"long_name": "Sea Water Kinetic Energy", "units": "J"},'
                            '"voupwspe": {"long_name": "Ekman Upwelling Speed", "units": "mm/s"},'
                            '"votkeavt": {"long_name": "Integrated Vertical Diffusivity", "units": "m2/s"},'
                            '"global":{"title": "monthly mean map",'
                            '"source": "copernicus med mfc toolbox or RR Reanalysis",'
                            '"institution": "MELODIES WP6 ACS INGV"}}')

# compute threshold

node = ET.SubElement(workflow, 'node')
node.set('id', 'df_threshold')
node.text = '\n'
node.tail = '\n'

ET.SubElement(node, 'job').set('id', 'jt_threshold')

sources = ET.SubElement(node, 'sources')
sources.text = '\n'
sources.tail = '\n'

source = ET.SubElement(sources, 'source')
source.set('refid', 'wf:node')
source.text = 'df_calc'
source.tail = '\n'

parameters = ET.SubElement(node, 'parameters')
parameters.text = '\n'
parameters.tail = '\n'

sPar(parameters, 'AttrStr', '{"thresholded_vodnsity": {"long_name": "Thresholded Sea Water Density",'
                            '"units": "dimensionless"},'
                            '"thresholded_vokenerg": {"long_name": "Thresholded Sea Water Kinetic Energy",'
                            '"units": "dimensionless"},'
                            '"thresholded_voupwspe": {"long_name": "Thresholded Ekman Upwelling Speed",'
                            '"units": "dimensionless"},'
                            '"thresholded_votkeavt": {"long_name": "Thresholded Integrated Vertical Diffusivity",'
                            '"units": "dimensionless"},'
                            '"global":{"title": "monthly mean thresholded map",'
                            '"source": "copernicus med mfc toolbox or RR Reanalysis",'
                            '"institution": "MELODIES WP6 ACS INGV"}}')

# ET.dump(application)
print ET.tostring(application)
