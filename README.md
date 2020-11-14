## EOEPCA - Vegetation index

[![Build Status](https://travis-ci.com/EOEPCA/app-vegetation-index.svg?branch=master)](https://travis-ci.com/EOEPCA/app-vegetation-index)

### About this application

This is a simple application used as an artifact for testing EOEPCA release 0.2

It validates the fan-out with stage-in paradigm where Sentinel-2 acquisitions staged as a STAC local catalog are processed to produce the NBR, NDVI and NDWI vegetation indexes.  

### Build the docker

The repo contains a Dockerfile and a Jenkinsfile.  

The build is done by Terradue's Jenkins instance with the configured job https://build.terradue.com/job/containers/job/eoepca-vegetation-index/

### Create the application package

Run the command below to print the CWL: 

```bash
docker run --rm -it terradue/eoepca-vegetation-index:0.1 vegetation-index-cwl --docker 'terradue/eoepca-vegetation-index:0.1'
```

Save the CWL output to a file called `eoepca-vegetation-index.cwl`

Package it as an application package wrapped in an Atom file with:

```bash
cwl2atom eoepca-vegetation-index.cwl > eoepca-vegetation-index.atom 
```

Post the Atom on the EOEPCA resource manager

### Application execution

#### Stage-in

Create a YAML file with:

instac.yml
```yaml
store_username: ''
store_apikey: ''
input_reference:
- https://earth-search.aws.element84.com/v0/collections/sentinel-s2-l2a-cogs/items/S2B_36RTT_20191205_0_L2A 
```

Stage the STAC item as a local STAC catalog with:

```console
cwltool instac.cwl instac.yml
```

Check the output and copy the results path (e.g. `/workspace/eoepca/app-vegetation-index/ugikjiux`)

#### Running the application

Create a YAML file with:

vegetation-index.yml
```yaml
aoi: 'POLYGON((30.358 29.243,30.358 29.545,30.8 29.545,30.8 29.243,30.358 29.243))'
input_reference:
- class: Directory
  path: file:///workspace/eoepca/app-vegetation-index/ugikjiux
```

Run the application with:

```console
cwltool vegetation-index.cwl#vegetation-index vegetation-index.yml
```

### Development

Create the conda environment with:

```console
conda env create -f environment.yml
```

Install the `vegetation-index` executable with:

```console
python setup.py install
```

Check the installation with:

```console
vegetation-index --help
```