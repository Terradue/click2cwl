# Copyright 2020 Terradue
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

baseCommand: test1
class: CommandLineTool
cwlVersion: v1.0
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
    type: string
  conf_file:
    inputBinding:
      position: 3
      prefix: --file
    type: File
  mode:
    inputBinding:
      position: 4
      prefix: --mode
    type:
    - 'null'
    - symbols:
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
      PATH: /Applications/miniforge3/envs/env_vi/bin:/Applications/miniforge3/condabin:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin
      a: '1'
      b: '2'
  ResourceRequirement:
    ramMax: 1
    ramMin: 2
stderr: std.err
stdout: std.out
