$graph:
- baseCommand: stage-in
  arguments: ['-t', './']
  class: CommandLineTool
  hints:
    DockerRequirement:
      dockerPull: stage
  id: stagein
  inputs:
    inp1:
      inputBinding:
        position: 1
        prefix: -u
      type: string
    inp2:
      inputBinding:
        position: 2
        prefix: -p
      type: string
    inp3:
      inputBinding:
        position: 3
      type: string[]
  outputs:
    results:
      outputBinding:
        glob: .
      type: Any
  requirements:
    EnvVarRequirement:
      envDef:
        PATH: /opt/anaconda/envs/env_stagein/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
    ResourceRequirement: {}
  stderr: std.err
  stdout: std.out
- class: Workflow
  label: Instac stage-in
  doc: Stage-in using Instac
  id: main
  inputs:
    input_reference:
      doc: A reference to an opensearch catalog
      label: A reference to an opensearch catalog
      type: string[]
    store_username:
      type: string
    store_apikey:
      type: string
  outputs:
  - id: wf_outputs
    outputSource:
    - node_1/results
    type:
      items: Directory
      type: array
  steps:
    node_1:
      in:
        inp1: store_username
        inp2: store_apikey
        inp3: input_reference
      out:
      - results
      run: '#stagein'
cwlVersion: v1.0

