$graph:
- baseCommand: vegetation-index
  class: CommandLineTool
  hints:
    DockerRequirement:
      dockerPull: dockerPull = wps3-runner:0.1
  id: clt
  inputs:
  - inp1:
      inputBinding:
        position: 1
        prefix: --input_reference
      type: Directory
  - inp2:
      inputBinding:
        position: 2
        prefix: --aoi
      type: string?
  outputs:
    results:
      outputBinding:
        glob: .
      type: Directory
  requirements:
    EnvVarRequirement:
      envDef:
        PATH: /home/farid/anaconda3/envs/env_vi/bin:/home/farid/anaconda3/condabin:/home/farid/.local/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games:/snap/bin
    ResourceRequirement: {}
  stderr: std.err
  stdout: std.out
- class: Workflow
  doc: hello I'm the doc of Workflow class
  id: vegetation-index
  inputs:
    aoi:
      doc: aoi doc
      label: aoi label
      type: string?
    input_reference:
      doc: input_reference doc
      label: input_reference label
      type: Directory
  label: hello I'm the label of Workflow class
  outputs:
    id: wf_outputs
    outputSource: node_1/results
    type: Directory
  steps:
    node_1:
      in:
        inp1: input_reference
        inp2: aoi
      out: results
      run: '#clt'
cwlVersion: v1.0
