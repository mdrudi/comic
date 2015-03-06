# Intro 
The **C**alculator f**O**r **M**arine **I**ndicators and **C**haracteristics - **COMIC** - is a software under development into the work package 
[WP6 Assessmento of Good Environmental Status for the oceans and seas] (http://www.melodiesproject.eu/node/35), 
in project [MELODIES - http://www.melodiesproject.eu] (http://www.melodiesproject.eu) . 

**The MELODIES project - Maximizing the Exploitation of Linked Open Data In Enterprise and Science** : 
this project aims to demonstrate the business and scientific benefits of releasing data openly through real applications .

**WP6 Assessment of Good Environmental Status for the oceans and seas** : a new services in development 
within the MELODIES project, for the assessment of GES (Good Environmental Status) and support its achievement 
by 2020 as defined in [Marine Strategy Framework Directive - DIRECTIVE 2008/56/EC OF THE EUROPEAN PARLIAMENT AND OF THE COUNCIL] (http://ec.europa.eu/environment/marine/eu-coast-and-marine-policy/marine-strategy-framework-directive/index_en.htm)

## Acknowledgements

...


# COMIC

This software aims to compute *GES characteristics and indicators* from *multi-year Earth Observation and Model datasets*, available as [open data](https://open-data.europa.eu/en/data) 

The initial design took into consideration issues related to the huge volume of available inputs, 
hence the **performance requirements**, due to some kind of applications, 
and the **efficiency** in computation and data access, due to the growing relevance of the [sustainability](http://ec.europa.eu/environment/eussd/) issue. 
The development is based as much as possible on criteria for software and technology **reusability**.   


## Content of repository

The executable program is :
```
src/main/python/sp/sp.py
```

Repository content :
```
.
\-- src
    \-- main
        |-- app-resources   -> additional software required in project environment
        |-- doc             -> some documentation
        |-- python
        |   \-- sp          -> source code of the software
        \-- resources       -> procedure to deploy in project environment
```


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

List of prerequisites for this software execution :

* NetCDF library - test done with version 4.1.1
* HDF5 library - test done with version 1.8.5
* Python - test done with version 2.6.6
* numpy - test done with version 1.4.1
* netcdf4-python - test done with version 1.0.2


## Quick Usage Examples

The following examples are only meant to show in short some simple usage of this program.

To compute the map of mean _votemper_ field at depth layers (parameter --oav) [0,20] , [20,75] and [75,150] in a given lon/lat box (parameter --ilonlat). The input field is available in one nc file _/path/filename.nc_ at any depth layers.
```
sp.py --ifile /path/filename.nc --ifield=votemper --ilonlat='[  [[12.75, 13.0], [44.5, 45.5]] , [[12.9,13.8],[44.3,45]] ]' --oav='[0,20,75,150]'
```

To compute the maps of mean _votemper_ field at depth layers (parameter --oav) [0,20] , [20,75] and [75,150] in a given lon/lat box (parameter --ilonlat). The input fields are available in many nc files which are listed in  _/path/listinputfiles.txt_ . The program will perform the same computation on each input file and output one output file for each input file.
```
sp.py --ifile list --ifield=votemper --ilonlat='[  [[12.75, 13.0], [44.5, 45.5]] , [[12.9,13.8],[44.3,45]] ]' --oav='[0,20,75,150]' < /path/listinputfiles.txt
```

To compute the map of mean _votemper_ field over the time. The input fields are available in many nc files which are listed in  _/path/listinputfiles.txt_ and must cover a continuous temporal range.
```
sp.py --ifile list --ifield=votemper --oat < /path/listinputfiles.txt
```

To compute the time-series (parameter --otc) of mean value over the whole horizontal domain (parameter --oao) of _votemper_ field. The input fields are available in many nc files which are listed in  _/path/listinputfiles.txt_ and must cover a continuous temporal range. 
```
sp.py --ifile list --ifield=votemper --oao --otc < /path/listinputfiles.txt
```
