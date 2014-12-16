This software is under development into the work package 
[WP6 Assessmento of Good Environmental Status for the oceans and seas] (http://www.melodiesproject.eu/node/35), 
in project [MELODIES - http://www.melodiesproject.eu] (http://www.melodiesproject.eu) . 

**The MELODIES project - Maximizing the Exploitation of Linked Open Data In Enterprose and Science** : 
Aims to demonstrate the business and scientific benefits of releasing data openly through real applications .

**WP6 Assessmento of Good Environmental Status for the oceans and seas** : a new services in development 
within the MELODIES project, for the assessment of GES (Good Environmental Status) and support its achievement 
by 2020 as defined in [Marine Strategy Framework Directive - DIRECTIVE 2008/56/EC OF THE EUROPEAN PARLIAMENT AND OF THE COUNCIL] (http://ec.europa.eu/environment/marine/eu-coast-and-marine-policy/marine-strategy-framework-directive/index_en.htm)


# Interpolation Toolbox

Toolbox aims to compute GES characteristics and indicators. 

The initial design took into consideration issues related to the huge volume of available data for input, 
hence the performance requirements in such kind of application, and the efficiency in computation and data access, 
due to the growing relevance of the [sustainability](http://ec.europa.eu/environment/eussd/) issue. 
The development is based as much as possible on criteria for software and technology reusability.   


## Stakeholders

...


## Features

The following list is going to be updated during the development.

Functional :

* possible to select the working area in terms of lon/lat boxes
* possible output : map or time-series
* possible to perform one or more of the following computation 
	* average over spatial vertical dimension 
	* average over time 
	* average over spatial horizontal dimension

Technical :

* possible to provide the input by means of a stream of filename through the standard input (stdio) at execution time
* possible to implement a Map/Reduce workflow
* adopted standard : 
	* output in file format NetCDF4, convention CF-1.6
* possible to output benchmarking information
* possible to activate memory efficient working mode


## Development environment

Following the list of prerequisites for this software execution :

* NetCDF library - test done with version 4.1.1
* HDF5 library - test done with version 1.8.5
* Python - test done with version 2.6.6
* numpy - test done with version 1.4.1
* netcdf4-python - test done with version 1.0.2


## Content of repository


```
.
\-- src
    \-- main
        |-- app-resources   -> additional software required in the execution environment
        |-- doc             -> some documentation
        |-- python
        |   \-- sp          -> source code of the software
        \-- resources       -> procedure to deploy the software in the execution environment
```

