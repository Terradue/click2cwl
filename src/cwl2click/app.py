import sys
import logging
import click
from .click2cwl import Click2CWL
from .cwl_constructor import CwlCreator
from .cwlparam import CWLParam
from .clt import CommandLineTool
from .wf import Workflow
from .cwlexport import CWLExport
from .paramexport import ParamExport
import io

logging.basicConfig(stream=sys.stderr,
                    level=logging.DEBUG,
                    format='%(asctime)s %(levelname)-8s %(message)s',
                    datefmt='%Y-%m-%dT%H:%M:%S')


@click.command(short_help='hello Im the label of Workflow class',
               help='hello Im the doc of Workflow class',
               context_settings=dict(
                   ignore_unknown_options=True,
                   allow_extra_args=True, ))
@click.option('--input_reference', '-i', 'input_reference', type=click.Path(), help='this input reference', required=True)
@click.option('--aoi', '-a', 'aoi', help='help for the area of interest', default='POLYGON()', required=False)
@click.option('--file', '-f', 'conf_file', help='help for the conf file', type=click.File(mode='w'))
@click.option('--mode', '-m', 'mode', type=click.Choice(['local', 'ftp']), required=False)
@click.pass_context
def entry(ctx, **kwargs):

    click2cwl = Click2CWL(ctx, kwargs)

    if click2cwl.extra_params:   
        
        if click2cwl.extra_params['dump'] == 'cwl':

            CWLExport(click2cwl).dump()
        
        else:

            ParamExport(click2cwl).dump()
        

    sys.exit(1)

    print(dir(ctx.command))

    click2cwl = Click2CWL(ctx, kwargs)

    clt = CommandLineTool(obj)

    wf = Workflow(obj)

    print(clt.to_dict())

    print(wf.to_dict())        

    sys.exit(1)
    print([param.type for param in ctx.command.params])
 

    for index, param in enumerate(ctx.command.params):
        
        cwl_param = CWLParam(param)
    
        print(cwl_param.to_clt_input(position=index+1))
        print(cwl_param.to_workflow_param())

    sys.exit(1)

    print([param.type for param in ctx.command.params])

    cwl_types = {}

    cwl_types[click.types.Path] = 'Directory'
    cwl_types[click.types.File] = 'File'
    cwl_types[click.types.StringParamType] = 'string'
    cwl_types[click.types.Choice] = 'enum'

    print([type(param.type) for param in ctx.command.params])
    print([cwl_types.get(type(param.type)) for param in ctx.command.params])

    print(str(ctx.command.params[0].type))
    print(isinstance(ctx.command.params[0].type, click.types.Path))

    #print(a[ctx.command.params[0].type])
    #print(ctx.command.params)

    #print(dict([(name, getattr(ctx.command.params[0], name)) for name in list(dir(ctx.command.params[0]))]))

    #print('opts', ctx.command.params[0].opts[0])
    #print('multiple', ctx.command.params[0].multiple)
    #print('required', ctx.command.params[0].required)
    #print('is_flag', ctx.command.params[0].is_flag)
    #print('help', ctx.command.params[0].help)
    print('type', ctx.command.params[3].type.choices)
    

    #print(dir(ctx.command.params[3]))
    sys.exit(1)
    print(ctx.command.params[0].name,
    ctx.command.params[0].help)

    obj = Click2CWL(ctx, kwargs)

    #print('business as usual ', ctx.args)

    # keys = [ctx.args[i][2:] for i in range(0, len(ctx.args), 2)]

    # extra_params = {}

    # extra_params['requirements'] = {}
    
    # for i in range(0, len(ctx.args), 2):

    #     key = ctx.args[i][2:]

    #     if key == 'requirement':
  
    #         extra_params['requirements'][ctx.args[i + 1].split('=')[0]] = ctx.args[i + 1].split('=')[1]
    
    #     else: 

    #         extra_params[key] = ctx.args[i + 1]


    #extra_params = {ctx.args[i][2:]: ctx.args[i + 1] for i in range(0, len(ctx.args), 2)}

    print(obj._extra_params)

    sys.exit(1)
    docker = requirement = env = scatter = None
    f = io.StringIO(str(ctx.command.params[2].name))
    f.close()


    if 'requirement' in extra_params.keys():
        requirement = get_key_and_value_of_extra_params(extra_params['requirement'])
    if 'env' in extra_params.keys():
        env = get_key_and_value_of_extra_params(extra_params['env'])
    if 'docker' in extra_params.keys():
        docker = extra_params['docker']
    if 'scatter' in extra_params.keys():
        scatter = get_key_and_value_of_extra_params(extra_params['scatter'])

    cwl_object = CwlCreator(ctx, docker=docker, requirements=requirement, env=env, scatter=scatter)
    if 'dump' in extra_params.keys():
        cwl_object.dump(extra_params['dump'])

    print(docker)

    sys.exit(0)

def get_key_and_value_of_extra_params(params):
    params_key_and_value = [x.strip() for x in params.split('=')]
    param_dict = {params_key_and_value[0]: params_key_and_value[1]}
    return param_dict

    
if __name__ == '__main__':
    entry()
