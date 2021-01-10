$graph:
- baseCommand: vegetation-index
  class: CommandLineTool
  hints:
    DockerRequirement:
      dockerPull: veg-index:0.1
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
  - inp3:
      inputBinding:
        position: 3
        prefix: --conf_file
      type: File?
  - inp4:
      inputBinding:
        position: 4
        prefix: --mode
      symbols:
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
      - PATH: /home/farid/anaconda3/bin:/home/farid/anaconda3/condabin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/snap/bin
      - test_env: path/to/env
    ResourceRequirement:
      ramMix: '8'
  stderr: std.err
  stdout: std.out
- class: Workflow
  doc: hello Im the doc of Workflo class
  id: vegetation-index
  inputs:
    aoi:
      doc: aoi doc
      label: aoi label
      type: string?
    conf_file:
      doc: conf_file doc
      label: conf_file label
      type: File?
    input_reference:
      doc: input_reference doc
      label: input_reference label
      type: Directory
    mode:
      symbols:
      - local
      - ftp
      type: enum
  label: hello Im the label of Workflo class
  outputs:
    id: wf_outputs
    outputSource: node_1/results
    type: Directory
  steps:
    node_1:
      in:
        inp1: input_reference
        inp2: aoi
        inp3: conf_file
        inp4: mode
      out: results
      run: '#clt'
cwlVersion: v1.0
