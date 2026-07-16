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

cwlVersion: v1.0
baseCommand: Stars
doc: "Run Stars for staging data"
class: CommandLineTool
hints:
  DockerRequirement:
    dockerPull: ghcr.io/terradue/stars:latest
id: stars
arguments:
- copy
- --harvest
- -v
- -rel
- -r
- '4'
- -o
- ./
inputs: 
  IN_S3_SERVICEURL: 
    type: string?
  IN_S3_ACCESS_KEY_ID:
    type: string?
  IN_S3_SECRET_ACCESS_KEY:
    type: string?
outputs: {}
requirements:
  EnvVarRequirement:
    envDef:
      PATH: /usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
      AWS__ServiceURL: $(inputs.IN_S3_SERVICEURL)
      AWS_ACCESS_KEY_ID: $(inputs.IN_S3_ACCESS_KEY_ID)
      AWS_SECRET_ACCESS_KEY: $(inputs.IN_S3_SECRET_ACCESS_KEY)
  ResourceRequirement: {}
