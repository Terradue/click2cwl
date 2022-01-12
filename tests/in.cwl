cwlVersion: v1.0
baseCommand: Stars
doc: "Run Stars for staging data"
class: CommandLineTool
hints:
  DockerRequirement:
    dockerPull: terradue/stars-t2:latest
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