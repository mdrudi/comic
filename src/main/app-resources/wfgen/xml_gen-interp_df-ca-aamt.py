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
sPar(defaultParameters, 'OutField', '', title="Output derived field", abstract="Example: vodnsity", scope="runtime")
sPar(defaultParameters, 'Var', '', title="Output Variable", abstract="Must be the same as OutField", scope="runtime")
sPar(defaultParameters, 'LonLat', 'None', title="WorkingArea", abstract="default None", scope="runtime")
sPar(defaultParameters, 'OutFile', '.out.nc')
sPar(defaultParameters, 'OutLayer', '[0,10,50,100,500,1000,2000]', title="DepthLayers",
     abstract="default [0,10,50,100,500,1000,2000]", scope="runtime")
sPar(defaultParameters, 'bm', 'True')
sPar(defaultParameters, 'iClean', 'True')

# monthly climatology template

jobTemplate = ET.SubElement(jobTemplates, 'jobTemplate')
jobTemplate.set('id', "jt_mon_clim")
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
sPar(defaultParameters, 'Var', '', title="Output Variable", abstract="Must be the same as OutField", scope="runtime")
sPar(defaultParameters, 'OutFile', '.out.nc')
sPar(defaultParameters, 'oac', 'True')
sPar(defaultParameters, 'bm', 'True')
sPar(defaultParameters, 's', 'True')
sPar(defaultParameters, 'iClean', 'True')

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
sPar(defaultParameters, 'Var', '', title="Output Variable", abstract="Must be the same as OutField", scope="runtime")
sPar(defaultParameters, 'oac', 'True')
sPar(defaultParameters, 'bm', 'True')
sPar(defaultParameters, 'iClean', 'True')

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
sPar(defaultParameters, 'Var', '', title="Output Variable", abstract="Must be the same as OutField", scope="runtime")
sPar(defaultParameters, 'oao', 'True')
sPar(defaultParameters, 'otc', 'True')
sPar(defaultParameters, 'bm', 'True')
sPar(defaultParameters, 'iClean', 'True')

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
sPar(defaultParameters, 'Var', '', title="Output Variable", abstract="Must be the same as OutField", scope="runtime")
sPar(defaultParameters, 'OutFile', '.out.nc')
sPar(defaultParameters, 'oat', '[]')
sPar(defaultParameters,  'bm', 'True')
sPar(defaultParameters, 's', 'True')
sPar(defaultParameters, 'iClean', 'True')

# derived field climatology and average annual mean timeseries workflow

workflow = ET.SubElement(application, 'workflow')
workflow.set('id', 'wp6_wf_id')
workflow.set('title', 'WP6 derived field climatology and average annual mean timeseries workflow')
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

# compute climatology node_g split

node = ET.SubElement(workflow, 'node')
node.set('id', 'ca_input_split')
node.text = '\n'
node.tail = '\n'

ET.SubElement(node, 'job').set('id', 'jt_split')

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

sPar(parameters, 'GroupRange', '2')

# compute monthly climatology

node = ET.SubElement(workflow, 'node')
node.set('id', 'ca_mon_clim')
node.text = '\n'
node.tail = '\n'

ET.SubElement(node, 'job').set('id', 'jt_mon_clim')

sources = ET.SubElement(node, 'sources')
sources.text = '\n'
sources.tail = '\n'

source = ET.SubElement(sources, 'source')
source.set('refid', 'wf:node')
source.text = 'ca_input_split'
source.tail = '\n'

parameters = ET.SubElement(node, 'parameters')
parameters.text = '\n'
parameters.tail = '\n'

sPar(parameters, 'AttrStr', '{"vodnsity": {"long_name": "Sea Water Density", "units": "Kg/m3"},'
                            '"vokenerg": {"long_name": "Sea Water Kinetic Energy", "units": "J"},'
                            '"voupwspe": {"long_name": "Ekman Upwelling Speed", "units": "mm/s"},'
                            '"votkeavt": {"long_name": "Integrated Vertical Diffusivity", "units": "m2/s"},'
                            '"global":{"title": "monthly climatology map",'
                            '"source": "copernicus med mfc toolbox or RR Reanalysis",'
                            '"institution": "MELODIES WP6 ACS INGV"}}')

# compute annual climatology

node = ET.SubElement(workflow, 'node')
node.set('id', 'ca_an_clim')
node.text = '\n'
node.tail = '\n'

ET.SubElement(node, 'job').set('id', 'jt_an_clim')

sources = ET.SubElement(node, 'sources')
sources.text = '\n'
sources.tail = '\n'

source = ET.SubElement(sources, 'source')
source.set('refid', 'wf:node')
source.text = 'ca_mon_clim'
source.tail = '\n'

parameters = ET.SubElement(node, 'parameters')
parameters.text = '\n'
parameters.tail = '\n'

sPar(parameters, 'iKey', 'mapcomic2(.*)(\.nc$)')
sPar(parameters, 'OutFile', 'out_m_12.nc')
sPar(parameters, 'AttrStr', '{"vodnsity": {"long_name": "Sea Water Density", "units": "Kg/m3"},'
                            '"vokenerg": {"long_name": "Sea Water Kinetic Energy", "units": "J"},'
                            '"voupwspe": {"long_name": "Ekman Upwelling Speed", "units": "mm/s"},'
                            '"votkeavt": {"long_name": "Integrated Vertical Diffusivity", "units": "m2/s"},'
                            '"global":{"title": "annual climatology map",'
                            '"source": "copernicus med mfc toolbox or RR Reanalysis",'
                            '"institution": "MELODIES WP6 ACS INGV"}}')

# compute monthly basin mean timeseries

node = ET.SubElement(workflow, 'node')
node.set('id', 'ca_basin_m_ts')
node.text = '\n'
node.tail = '\n'

ET.SubElement(node, 'job').set('id', 'jt_basin_m_ts')

sources = ET.SubElement(node, 'sources')
sources.text = '\n'
sources.tail = '\n'

source = ET.SubElement(sources, 'source')
source.set('refid', 'wf:node')
source.text = 'ca_mon_clim'
source.tail = '\n'

parameters = ET.SubElement(node, 'parameters')
parameters.text = '\n'
parameters.tail = '\n'

sPar(parameters, 'iKey', 'mapcomic2(.*)(\.nc$)')
sPar(parameters, 'OutFile', 'out_ts_12.nc')
sPar(parameters, 'AttrStr', '{"vodnsity": {"long_name": "Sea Water Density", "units": "Kg/m3"},'
                            '"vokenerg": {"long_name": "Sea Water Kinetic Energy", "units": "J"},'
                            '"voupwspe": {"long_name": "Ekman Upwelling Speed", "units": "mm/s"},'
                            '"votkeavt": {"long_name": "Integrated Vertical Diffusivity", "units": "m2/s"},'
                            '"global":{"title": "monthly climatology timeseries",'
                            '"source": "copernicus med mfc toolbox or RR Reanalysis",'
                            '"institution": "MELODIES WP6 ACS INGV"}}')

# compute averaged annual mean timeseries node_g split

node = ET.SubElement(workflow, 'node')
node.set('id', 'aamt_input_split')
node.text = '\n'
node.tail = '\n'

ET.SubElement(node, 'job').set('id', 'jt_split')

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

sPar(parameters, 'GroupRange', '4')

# compute timeseries concatenation

node = ET.SubElement(workflow, 'node')
node.set('id', 'aamt_t_avg')
node.text = '\n'
node.tail = '\n'

ET.SubElement(node, 'job').set('id', 'jt_t_avg')

sources = ET.SubElement(node, 'sources')
sources.text = '\n'
sources.tail = '\n'

source = ET.SubElement(sources, 'source')
source.set('refid', 'wf:node')
source.text = 'aamt_input_split'
source.tail = '\n'

parameters = ET.SubElement(node, 'parameters')
parameters.text = '\n'
parameters.tail = '\n'

sPar(parameters, 'AttrStr', '{"vodnsity": {"long_name": "Sea Water Density", "units": "Kg/m3"},'
                            '"vokenerg": {"long_name": "Sea Water Kinetic Energy", "units": "J"},'
                            '"voupwspe": {"long_name": "Ekman Upwelling Speed", "units": "mm/s"},'
                            '"votkeavt": {"long_name": "Integrated Vertical Diffusivity", "units": "m2/s"},'
                            '"global":{"title": "annual mean map",'
                            '"source": "copernicus med mfc toolbox or RR Reanalysis",'
                            '"institution": "MELODIES WP6 ACS INGV"}}')

# compute annual basin mean timeseries

node = ET.SubElement(workflow, 'node')
node.set('id', 'aamt_basin_m_ts')
node.text = '\n'
node.tail = '\n'

ET.SubElement(node, 'job').set('id', 'jt_basin_m_ts')

sources = ET.SubElement(node, 'sources')
sources.text = '\n'
sources.tail = '\n'

source = ET.SubElement(sources, 'source')
source.set('refid', 'wf:node')
source.text = 'aamt_t_avg'
source.tail = '\n'

parameters = ET.SubElement(node, 'parameters')
parameters.text = '\n'
parameters.tail = '\n'

sPar(parameters, 'iKey', 'mapcomic4(.*)(\.nc$)')
sPar(parameters, 'OutFile', 'out4.nc')
sPar(parameters, 'AttrStr', '{"vodnsity": {"long_name": "Sea Water Density", "units": "Kg/m3"},'
                            '"vokenerg": {"long_name": "Sea Water Kinetic Energy", "units": "J"},'
                            '"voupwspe": {"long_name": "Ekman Upwelling Speed", "units": "mm/s"},'
                            '"votkeavt": {"long_name": "Integrated Vertical Diffusivity", "units": "m2/s"},'
                            '"global":{"title": "average annual mean timeseries",'
                            '"source": "copernicus med mfc toolbox or RR Reanalysis",'
                            '"institution": "MELODIES WP6 ACS INGV"}}')

# ET.dump(application)
print ET.tostring(application)
