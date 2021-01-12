$graph:
- baseCommand: test1
  class: CommandLineTool
  hints:
    DockerRequirement:
      dockerPull: aaa
  id: clt
  inputs:
    input_reference:
      inputBinding:
        position: 1
        prefix: --input_reference
      type: Directory
    aoi:
      inputBinding:
        position: 2
        prefix: --aoi
      type: string?
    conf_file:
      inputBinding:
        position: 3
        prefix: --file
      type: File?
    mode:
      inputBinding:
        position: 4
        prefix: --mode
      type:
      - 'null'
      - symbols: &id001
        - local
        - ftp
        type: enum
  outputs:
    results:
      outputBinding:
        glob: .
      type: Directory
  requirements:
    EnvVarRequirement:
      envDef:
        PATH: /opt/anaconda3/envs/env_click2cwl/bin:/opt/anaconda3/condabin:/Library/Frameworks/Python.framework/Versions/3.6/bin:/Library/Frameworks/Python.framework/Versions/3.7/bin:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin
        a: '1'
        b: '2'
    ResourceRequirement:
      ramMax: 1
      ramMin: 2
  stderr: std.err
  stdout: std.out
- class: Workflow
  doc: hello Im the doc of Workflow class
  id: test1
  inputs:
    input_reference:
      doc: this input reference
      label: this input reference
      type: Directory
    aoi:
      doc: help for the area of interest
      label: help for the area of interest
      type: string?
    conf_file:
      doc: help for the conf file
      label: help for the conf file
      type: File?
    mode:
      doc: null
      label: null
      type:
      - 'null'
      - symbols: *id001
        type: enum
  label: hello Im the label of Workflow class
  outputs:
  - id: wf_outputs
    outputSource:
    - step_1/results
    type: Directory
  steps:
    step_1:
      in:
        input_reference: input_reference
        aoi: aoi
        conf_file: conf_file
        mode: mode
      out:
      - results
      run: '#clt'
cwlVersion: v1.0
