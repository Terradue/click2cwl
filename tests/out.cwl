cwlVersion: v1.0
baseCommand: Stars
doc: "Run Stars for staging data"
class: CommandLineTool
hints:
  DockerRequirement:
    dockerPull: terradue/stars:latest
id: stars
arguments:
- copy
- -v
- -r
- '4'
inputs: 
  OUT_S3_SERVICEURL: 
    type: string?
  OUT_S3_ACCESS_KEY_ID: 
    type: string?
  OUT_S3_SECRET_ACCESS_KEY: 
    type: string?
  OUT_S3_REGION:
    type: string? 
  OUTPUT:
    type: string?
    inputBinding:
      position: 5
      prefix: -o
outputs: {}
requirements:
  EnvVarRequirement:
    envDef:
      PATH: /usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
      AWS__ServiceURL: $(inputs.OUT_S3_SERVICEURL)
      AWS_ACCESS_KEY_ID: $(inputs.OUT_S3_ACCESS_KEY_ID)
      AWS_SECRET_ACCESS_KEY: $(inputs.OUT_S3_SECRET_ACCESS_KEY)
      AWS__SignatureVersion: "2"
      AWS__Region: $(inputs.OUT_S3_REGION)
      AWS__AuthenticationRegion: $(inputs.OUT_S3_REGION)
  ResourceRequirement: {}
