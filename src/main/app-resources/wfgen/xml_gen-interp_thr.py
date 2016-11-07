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
sPar(defaultParameters, 'Threshold', '', title="Threshold scalar (float)", abstract="Example: 3e-06", scope="runtime")
sPar(defaultParameters, 'Var', '', title="Variable to be discriminated by threshold", abstract="Example: votkeavt",
     scope="runtime")

defaultJobconf = ET.SubElement(jobTemplate, 'defaultJobconf')
defaultJobconf.text = '\n'
defaultJobconf.tail = '\n'

# threshold workflow

workflow = ET.SubElement(application, 'workflow')
workflow.set('id', 'wp6_wf_id')
workflow.set('title', 'WP6 threshold workflow')
workflow.set('abstract', 'Toolbox parameters')
workflow.text = '\n'
workflow.tail = '\n'

workflowVersion = ET.SubElement(workflow, 'workflowVersion')
workflowVersion.text = '1.0'
workflowVersion.tail = '\n'

# compute threshold

node = ET.SubElement(workflow, 'node')
node.set('id', 'threshold')
node.text = '\n'
node.tail = '\n'

ET.SubElement(node, 'job').set('id', 'jt_threshold')

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

sPar(parameters, 'AttrStr', '{"thresholded_votemper": {"long_name": "Thresholded Temperature",'
                            '"units": "dimensionless"},'
                            '"thresholded_vosaline": {"long_name": "Thresholded Salinity",'
                            '"units": "dimensionless"},'
                            '"thresholded_vozocrtx": {"long_name": "Thresholded Zonal Velocity",'
                            '"units": "dimensionless"},'
                            '"thresholded_vomecrty": {"long_name": "Thresholded Meridional Velocity",'
                            '"units": "dimensionless"},'
                            '"thresholded_sozotaux": {"long_name": "Thresholded Zonal Wind Stress",'
                            '"units": "dimensionless"},'
                            '"thresholded_sometauy": {"long_name": "Thresholded Meridional Wind Stress",'
                            '"units": "dimensionless"},'
                            '"global":{"title": "thresholded map",'
                            '"source": "copernicus med mfc toolbox or RR Reanalysis",'
                            '"institution": "MELODIES WP6 ACS INGV"}}')

# ET.dump(application)
print ET.tostring(application)
