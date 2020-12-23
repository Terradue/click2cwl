baseCommand: vegetation-index
class: CommandLineTool
hints:
  DockerRequirement:
    dockerPull: to/docker
id: clt
inputs:
- inp1:
    inputBinding:
      position: 1
      prefix: --aoi
    type: Directory
- inp2:
    inputBinding:
      position: 2
      prefix: --input_reference
    type: String
outputs:
  results:
    outputBinding:
      glob: .
    type: Directory
requirements:
  EnvVarRequirement:
    envDef:
      PATH: /home/farid/anaconda3/envs/env_vi/bin:/home/farid/anaconda3/condabin:/home/farid/.local/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games:/snap/bin
  ResourceRequirement:
    myKey: my_val
stderr: std.err
stdout: std.out
class: Workflow
doc: hello I'm the doc of Workflow class
id: vegetation-index
inputs:
  aoi:
    doc: Area of interest in WKT
    id: aoi
    label: Area of interest
  input_reference:
    doc: EO product for vegetation index
    id: input_reference
    label: EO product for vegetation index
label: hello I'm the label of Workflow class
outputs:
  id: !!set
    wf_outputs: null
  outputSource: {}
  type: {}
steps:
  in: {}
  out: []
  run: []
