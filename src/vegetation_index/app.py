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
 
        sys.exit(0)

    print('business as usual')
    
    sys.exit(0)

def get_key_and_value_of_extra_params(params):
    params_key_and_value = [x.strip() for x in params.split('=')]
    param_dict = {params_key_and_value[0]: params_key_and_value[1]}
    return param_dict

    
if __name__ == '__main__':
    entry()
