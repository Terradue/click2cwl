## EOEPCA - Vegetation index

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

Use the parameters:

* **input_reference**:

    * https://catalog.terradue.com/sentinel2/search?uid=S2B_MSIL2A_20200130T004659_N0213_R102_T53HPA_20200130T022348
    * https://catalog.terradue.com/sentinel2/search?uid=S2A_MSIL2A_20191216T004701_N0213_R102_T53HPA_20191216T024808

* **aoi**: POLYGON((136.508 -36.108,136.508 -35.654,137.178 -35.654,137.178 -36.108,136.508 -36.108))
